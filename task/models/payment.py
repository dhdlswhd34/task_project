from django.db import models
from django.db.models import Q

from task.models.users import User


# 결제 정보
class Payment(models.Model):
    class Status(models.TextChoices):
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(db_comment="금액")
    payment_method = models.CharField(max_length=255, db_comment="결제방법")
    test = models.ForeignKey(
        "task_models.Test", null=True, blank=True, on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        "task_models.Course", null=True, blank=True, on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PAID,
        db_comment="상태",
    )
    paid_at = models.DateTimeField(auto_now_add=True, db_comment="결제시간")
    cancelled_at = models.DateTimeField(
        null=True, blank=True, db_comment="취소시간"
    )

    class Meta:
        constraints = [
            # test 또는 course 중 하나만 존재
            models.CheckConstraint(
                check=(
                    (Q(test__isnull=False) & Q(course__isnull=True))
                    | (Q(test__isnull=True) & Q(course__isnull=False))
                ),
                name="payment_xor_target",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["paid_at"]),
        ]
        app_label = "task_models"
