from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import get_object_or_404

from task.models.course import Course, CourseRegistration
from task.models.payment import Payment

from task.serializers.courses import CourseSerializer


# 수업 목록 조회
class CourseListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer

    def get_queryset(self):
        now = timezone.now()
        qs = Course.objects.annotate(
            registration_count=Count("registrations")
        ).order_by("-id")
        status_param = self.request.query_params.get("status")
        if status_param == "available":
            qs = qs.filter(start_at__lte=now, end_at__gte=now)

        sort = self.request.query_params.get("sort", "created")
        if sort == "popular":
            qs = qs.order_by("-registration_count", "-id")
        elif sort == "created":
            qs = qs.order_by("-reg_date", "-id")
        return qs


# 수업 신청
class CourseEnrollView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        amount = int(request.data.get("amount", 0))
        method = request.data.get("payment_method")
        course = get_object_or_404(Course, id=id)

        if not course.is_available():
            return Response(
                {"message": "수강 가능 기간이 아닙니다."}, status=400
            )

        with transaction.atomic():
            if CourseRegistration.objects.filter(
                user=request.user, course=course
            ).exists():
                return Response(
                    {"message": "이미 신청한 수업입니다."}, status=400
                )

            payment = Payment.objects.create(
                user=request.user,
                amount=amount,
                payment_method=method,
                course=course,
                status=Payment.Status.PAID,
            )
            CourseRegistration.objects.create(
                user=request.user,
                course=course,
                status=CourseRegistration.Status.ENROLLED,
            )
            return Response({"id": payment.id, "status": "paid"}, status=201)


# 수업 완료 처리
class CourseCompleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        course = get_object_or_404(Course, id=id)
        reg = get_object_or_404(
            CourseRegistration, user=request.user, course=course
        )
        if reg.status == CourseRegistration.Status.COMPLETED:
            return Response({"message": "이미 완료되었습니다."}, status=400)

        reg.status = CourseRegistration.Status.COMPLETED
        reg.completed_at = timezone.now()
        reg.save(update_fields=["status", "completed_at"])
        return Response({"message": "수업 수강 완료 처리되었습니다."})
