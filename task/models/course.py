from django.db import models, transaction
from django.utils import timezone

from task.models.users import User


# 수업
class Course(models.Model):
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
        app_label = "task_models"
        indexes = [
            models.Index(fields=["start_at", "end_at"]),
            models.Index(fields=["reg_date"]),
            models.Index(fields=["reg_count"]),
        ]


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

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        with transaction.atomic():
            super().save(*args, **kwargs)
            # 새로 등록
            if is_new:
                # 등록 추가
                self.course.reg_count = models.F("reg_count") + 1
                self.course.save(update_fields=["reg_count"])

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            course = self.course
            super().delete(*args, **kwargs)
            # 등록 감소
            course.reg_count = models.F("reg_count") - 1
            course.save(update_fields=["reg_count"])
