from typing import Any

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .models import Task, Theme


class FrontPageView(TemplateView):
    template_name = "priorities/front_page.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["themes"] = Theme.objects.all()

        return context


class ManagementView(TemplateView):
    template_name = "priorities/management.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["themes"] = Theme.objects.all()

        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "priorities/management/task.html"
    context_object_name = "task"


class TaskCreateView(CreateView):
    model = Task
    template_name = "priorities/task_create.html"
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse_lazy("priorities:task_detail", kwargs={"pk": self.object.pk})


class TaskUpdateDeleteView(UpdateView):
    model = Task
    template_name = "priorities/task_update.html"
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse_lazy("priorities:task_detail", kwargs={"pk": self.object.pk})

    # TODO: implement recycle bin
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then return empty 200 response for HTMX.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse()
