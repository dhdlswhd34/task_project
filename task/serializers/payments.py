from rest_framework import serializers

from task.models.payment import Payment
from task.models.test import TestRegistration
from task.models.course import CourseRegistration


# 결제 정보
class PaymentSerializer(serializers.ModelSerializer):
    target_type = serializers.SerializerMethodField()
    target_title = serializers.SerializerMethodField()
    activity_time = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "payment_method",
            "status",
            "paid_at",
            "cancelled_at",
            "target_type",
            "target_title",
            "activity_time",
            "is_completed",
        ]

    def get_target_type(self, obj):
        return "test" if obj.test_id else "course"

    def get_target_title(self, obj):
        if obj.test_id:
            return obj.test.title
        if obj.course_id:
            return obj.course.title
        return None

    def get_activity_time(self, obj):
        if obj.test_id:
            reg = TestRegistration.objects.filter(
                user=obj.user, test=obj.test
            ).first()
            return reg.applied_at if reg else None
        if obj.course_id:
            reg = CourseRegistration.objects.filter(
                user=obj.user, course=obj.course
            ).first()
            return reg.enrolled_at if reg else None
        return None

    # 완료 확인
    def get_is_completed(self, obj):
        if obj.test_id:
            reg = TestRegistration.objects.filter(
                user=obj.user, test=obj.test
            ).first()
            return (
                reg.status == TestRegistration.Status.COMPLETED
                if reg
                else False
            )

        if obj.course_id:
            reg = CourseRegistration.objects.filter(
                user=obj.user, course=obj.course
            ).first()
            return (
                reg.status == CourseRegistration.Status.COMPLETED
                if reg
                else False
            )

        return False
