from django import forms

from .models import Feature, Task


class NewTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "priority", "deadline", "theme", "feature")
        widgets = {
            "theme": forms.HiddenInput(),
            "feature": forms.HiddenInput(),
        }


class NewFeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ("name", "description", "priority", "deadline", "goal")
        widgets = {
            "goal": forms.HiddenInput(),
        }
