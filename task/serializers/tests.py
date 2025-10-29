from rest_framework import serializers

from task.models.test import Test, TestRegistration


# 시험 정보
class TestSerializer(serializers.ModelSerializer):
    registration_count = serializers.IntegerField(read_only=True)
    is_available = serializers.SerializerMethodField()
    applied = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "id",
            "title",
            "start_at",
            "end_at",
            "reg_date",
            "registration_count",
            "is_available",
            "applied",
        ]

    def get_is_available(self, obj):
        return obj.is_available()

    def get_applied(self, obj):
        user = self.context["request"].user
        return TestRegistration.objects.filter(user=user, test=obj).exists()
