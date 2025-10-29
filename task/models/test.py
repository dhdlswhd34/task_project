from django.db import models
from django.utils import timezone

from task.models.users import User


# 시험
class Test(models.Model):
    title = models.CharField(max_length=255, db_comment="제목")
    start_at = models.DateTimeField(db_comment="시작")
    end_at = models.DateTimeField(db_comment="마지막")
    reg_date = models.DateTimeField(auto_now_add=True, db_comment="등록일")

    def is_available(self, now=None):
        now = now or timezone.now()
        return self.start_at <= now <= self.end_at

    class Meta:
        app_label = "task_models"


# 시험 등록
class TestRegistration(models.Model):
    class Status(models.TextChoices):
        APPLIED = "applied", "Applied"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="registrations"
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.APPLIED,
        db_comment="상태",
    )
    applied_at = models.DateTimeField(auto_now_add=True, db_comment="응시시간")
    completed_at = models.DateTimeField(
        null=True, blank=True, db_comment="완료시간"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "test"], name="uniq_user_test"
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["test"]),
        ]
        app_label = "task_models"
