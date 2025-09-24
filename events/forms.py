from django import forms

from events.models import Idea, EventRequest


class CreateIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = (
            "title",
            "overview",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Idea Title'
        })
        self.fields['overview'].widget = forms.Textarea(attrs={
           'class': 'form-control',
           'placeholder': 'Idea Overview'
        })



class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        fields = ["title", "overview", "start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter event title"}),
            "overview": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Brief event overview"}),
        }
