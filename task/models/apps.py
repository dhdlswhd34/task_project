from django.apps import AppConfig


class ModelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "task.models"
    label = "task_models"

    def ready(self):
        from task.models import users, test, course, payment
