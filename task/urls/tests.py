from django.urls import path
from task.views import tests

urlpatterns = [
    path("", tests.TestListView.as_view(), name="test_list"),
    path("/<int:id>/apply", tests.TestApplyView.as_view(), name="test_apply"),
    path(
        "/<int:id>/complete",
        tests.TestCompleteView.as_view(),
        name="test_complete",
    ),
]
