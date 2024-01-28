from django.urls import path

from . import views

app_name = "priorities"

urlpatterns = [
    path("management/", views.ManagementView.as_view(), name="management"),
    path("", views.FrontPageView.as_view(), name="front_page"),
    path("task/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("task/create/", views.TaskCreateView.as_view(), name="task_create"),
    path(
        "task/<int:pk>/update/",
        views.TaskUpdateDeleteView.as_view(),
        name="task_update_delete",
    ),
]
