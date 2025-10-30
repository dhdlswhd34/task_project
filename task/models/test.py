from django.db import models, transaction
from django.utils import timezone

from task.models.users import User


# 시험
class Test(models.Model):
    title = models.CharField(max_length=255, db_comment="제목")
    start_at = models.DateTimeField(db_comment="시작")
    end_at = models.DateTimeField(db_comment="마지막")
    reg_date = models.DateTimeField(auto_now_add=True, db_comment="등록일")
    reg_count = models.PositiveIntegerField(
        default=0, db_index=True, db_comment="등록개수"
    )

    def is_available(self, now=None):
        now = now or timezone.now()
        return self.start_at <= now <= self.end_at

    class Meta:
        indexes = [
            models.Index(fields=["start_at", "end_at"]),
            models.Index(fields=["reg_date"]),
            models.Index(fields=["reg_count"]),
        ]
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

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        with transaction.atomic():
            super().save(*args, **kwargs)
            # 새로 등록
            if is_new:
                # 등록 증가
                self.test.reg_count = models.F("reg_count") + 1
                self.test.save(update_fields=["reg_count"])

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            test = self.test
            super().delete(*args, **kwargs)
            # 등록 감소
            test.reg_count = models.F("reg_count") - 1
            test.save(update_fields=["reg_count"])
