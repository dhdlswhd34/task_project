from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

from task.models.payment import Payment
from task.models.test import TestRegistration
from task.models.course import CourseRegistration

from task.serializers.payments import PaymentSerializer


# 결제 내역 조회
class MyPaymentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        qs = Payment.objects.select_related("test", "course").filter(
            user=self.request.user
        )

        status_param = self.request.query_params.get("status")
        if status_param in (Payment.Status.PAID, Payment.Status.CANCELLED):
            qs = qs.filter(status=status_param)

        date_from = self.request.query_params.get("from")
        date_to = self.request.query_params.get("to")

        # paid_at 기준
        if date_from:
            qs = qs.filter(paid_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(paid_at__date__lte=date_to)

        return qs.order_by("-paid_at")


# 결제 취소
class PaymentCancelView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        payment = get_object_or_404(Payment, id=id, user=request.user)

        if payment.status != Payment.Status.PAID:
            return Response({"message": "이미 취소된 결제입니다."}, status=400)

        # 완료 여부 확인
        if payment.test_id:
            reg = TestRegistration.objects.filter(
                user=request.user, test_id=payment.test_id
            ).first()
            if reg and reg.status == TestRegistration.Status.COMPLETED:
                return Response(
                    {"message": "완료된 응시는 취소할 수 없습니다."},
                    status=400,
                )
        if payment.course_id:
            reg = CourseRegistration.objects.filter(
                user=request.user, course_id=payment.course_id
            ).first()
            if reg and reg.status == CourseRegistration.Status.COMPLETED:
                return Response(
                    {"message": "완료된 수강은 취소할 수 없습니다."},
                    status=400,
                )

        with transaction.atomic():
            # 관련 등록 삭제
            if payment.test_id:
                TestRegistration.objects.filter(
                    user=request.user, test_id=payment.test_id
                ).delete()
            if payment.course_id:
                CourseRegistration.objects.filter(
                    user=request.user, course_id=payment.course_id
                ).delete()

            payment.status = Payment.Status.CANCELLED
            payment.cancelled_at = timezone.now()
            payment.save(update_fields=["status", "cancelled_at"])

        return Response(
            {
                "message": "결제가 취소되었습니다.",
                "id": payment.id,
                "status": payment.status,
            }
        )
