from rest_framework import serializers

from task.models.course import Course, CourseRegistration


# 강의 정보
class CourseSerializer(serializers.ModelSerializer):
    registration_count = serializers.IntegerField(read_only=True)
    is_available = serializers.SerializerMethodField()
    enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "start_at",
            "end_at",
            "reg_date",
            "registration_count",
            "is_available",
            "enrolled",
        ]

    def get_is_available(self, obj):
        return obj.is_available()

    def get_enrolled(self, obj):
        user = self.context["request"].user
        return CourseRegistration.objects.filter(
            user=user, course=obj
        ).exists()
