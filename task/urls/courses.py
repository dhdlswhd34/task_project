from django.urls import path
from task.views import courses

urlpatterns = [
    path("", courses.CourseListView.as_view(), name="course_list"),
    path(
        "/<int:id>/enroll",
        courses.CourseEnrollView.as_view(),
        name="course_enroll",
    ),
    path(
        "/<int:id>/complete",
        courses.CourseCompleteView.as_view(),
        name="course_complete",
    ),
]
