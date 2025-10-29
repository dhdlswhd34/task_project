from django.db import models
from django.utils import timezone

from task.models.users import User


# 수업
class Course(models.Model):
    title = models.CharField(max_length=255, db_comment="제목")
    start_at = models.DateTimeField(db_comment="시작")
    end_at = models.DateTimeField(db_comment="마지막")
    reg_date = models.DateTimeField(auto_now_add=True, db_comment="등록일")

    def is_available(self, now=None):
        now = now or timezone.now()
        return self.start_at <= now <= self.end_at

    class Meta:
        app_label = "task_models"


# 수업 등록
class CourseRegistration(models.Model):
    class Status(models.TextChoices):
        ENROLLED = "enrolled", "Enrolled"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="registrations",
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.ENROLLED,
        db_comment="상태",
    )
    enrolled_at = models.DateTimeField(
        auto_now_add=True, db_comment="수강신청시간"
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, db_comment="완료시간"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="uniq_user_course"
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["course"]),
        ]
        app_label = "task_models"
