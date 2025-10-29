from django.urls import path
from task.views.users import SignupView, LoginView

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
]
