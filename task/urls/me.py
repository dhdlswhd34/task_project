from django.urls import path
from task.views import payments

urlpatterns = [
    path(
        "/payments",
        payments.MyPaymentListView.as_view(),
        name="my_payments",
    ),
]
