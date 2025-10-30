from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction
from django.db.models import Exists, OuterRef
from django.utils import timezone
from django.shortcuts import get_object_or_404

from task.models.test import Test, TestRegistration
from task.models.payment import Payment

from task.serializers.tests import TestSerializer


# 시험 목록 조회
class TestListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TestSerializer

    def get_queryset(self):
        now = timezone.now()

        applied_subquery = TestRegistration.objects.filter(
            user=self.request.user, test=OuterRef("pk")
        )
        queryset = Test.objects.annotate(applied=Exists(applied_subquery))

        # 필터링
        status = self.request.query_params.get("status")
        if status == "available":
            queryset = queryset.filter(start_at__lte=now, end_at__gte=now)

        # 정렬
        sort = self.request.query_params.get("sort", "created")
        if sort == "popular":
            queryset = queryset.order_by("-reg_count", "-id")
        else:
            queryset = queryset.order_by("-reg_date")

        return queryset


# 시험 응시 신청
class TestApplyView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        amount = int(request.data.get("amount", 0))
        method = request.data.get("payment_method")
        test = get_object_or_404(Test, id=id)

        if not test.is_available():
            return Response(
                {"message": "응시 가능 기간이 아닙니다."}, status=400
            )

        with transaction.atomic():
            # 이미 신청했는지 (UniqueConstraint로도 보장되지만 UX용 선체크)
            if TestRegistration.objects.filter(
                user=request.user, test=test
            ).exists():
                return Response(
                    {"message": "이미 신청한 시험입니다."}, status=400
                )

            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                payment_method=method,
                test=test,
                status=Payment.Status.PAID,
            )
            TestRegistration.objects.create(
                user=request.user,
                test=test,
                status=TestRegistration.Status.APPLIED,
            )
            return Response({"id": payment.id, "status": "paid"}, status=201)


# 시험 완료 처리
class TestCompleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        test = get_object_or_404(Test, id=id)
        reg = get_object_or_404(TestRegistration, user=request.user, test=test)
        if reg.status == TestRegistration.Status.COMPLETED:
            return Response({"message": "이미 완료되었습니다."}, status=400)

        reg.status = TestRegistration.Status.COMPLETED
        reg.completed_at = timezone.now()
        reg.save(update_fields=["status", "completed_at"])
        return Response({"message": "시험 응시 완료 처리되었습니다."})
