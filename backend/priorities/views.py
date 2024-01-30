from typing import Any

from django.db.models import ProtectedError
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .forms import NewFeatureForm, NewTaskForm
from .models import Feature, Goal, Task, Theme


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
    template_name = "priorities/management/task_form.html"
    form_class = NewTaskForm

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()

        if pk := self.request.GET.get("feature"):
            initial["feature"] = Feature.objects.get(pk=pk)
        elif pk := self.request.GET.get("theme"):
            initial["theme"] = Theme.objects.get(pk=pk)

        return initial

    def get_success_url(self) -> str:
        return reverse("priorities:task_detail", kwargs={"pk": self.object.pk})


class TaskUpdateDeleteView(UpdateView):
    model = Task
    template_name = "priorities/management/task_form.html"
    fields = ("name", "description", "priority", "deadline")

    def get_success_url(self) -> str:
        return reverse("priorities:task_detail", kwargs={"pk": self.object.pk})

    # TODO: implement recycle bin
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then return empty 200 response for HTMX.
        """
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse()


class FeatureDetailView(DetailView):
    model = Feature
    template_name = "priorities/management/feature.html"
    context_object_name = "feature"


class FeatureCreateView(CreateView):
    model = Feature
    template_name = "priorities/management/feature_form.html"
    form_class = NewFeatureForm

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()

        if pk := self.request.GET.get("goal"):
            initial["goal"] = Goal.objects.get(pk=pk)

        return initial

    # TODO: this should change depending on HTMX header presence
    # also the same for other views
    def get_success_url(self) -> str:
        return reverse("priorities:feature_detail", kwargs={"pk": self.object.pk})


class FeatureUpdateDeleteView(UpdateView):
    model = Feature
    template_name = "priorities/management/feature_form.html"
    fields = ("name", "description", "priority", "deadline")

    def get_success_url(self) -> str:
        return reverse("priorities:feature_detail", kwargs={"pk": self.object.pk})

    # TODO: implement recycle bin
    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then return empty 200 response for HTMX.
        """
        try:
            self.get_object().delete()
            return HttpResponse()
        except ProtectedError:
            return HttpResponse("Make sure to delete any children first", status=400)
