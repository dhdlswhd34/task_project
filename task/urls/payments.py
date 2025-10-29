from django.urls import path
from task.views import payments

urlpatterns = [
    path(
        "/<int:id>/cancel",
        payments.PaymentCancelView.as_view(),
        name="payment_cancel",
    ),
]
