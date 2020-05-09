from django import forms
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from . import models
from django.forms.models import inlineformset_factory
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget
from bootstrap_datepicker_plus import DatePickerInput


class CustomMapWidget(LeafletWidget):
    template_name = "problem_map/custom_map_widget.html"

class RelatedPersonForm(forms.ModelForm):

    class Meta:
        model = models.Person
        exclude = ["ip"]

class ProblemTypeForm(forms.ModelForm):
    thematic_field = forms.ModelMultipleChoiceField(
        queryset=models.ThematicField.objects.all(),
        label="Tematik Alan",
        required=True,
        widget=ModelSelect2MultipleWidget(
            model=models.ThematicField,
            queryset = models.ThematicField.objects.all(),
            search_fields=["name__icontains"],
            max_results = 100,
                          attrs = {
                "data-minimum-input-length": 0,
            }
        )
    )

    class Meta:
        model = models.ProblemType
        fields = ["name", "thematic_field"]



class ProblemForm(forms.ModelForm):
    location = PointField(required=False,
                          widget=CustomMapWidget)
    occurrence_date = forms.DateField(widget=DatePickerInput(format="%d-%m-%Y"))
    related_problem_type = forms.ModelChoiceField(
        queryset=models.ProblemType.objects.filter(is_approved=True),
        label="Problem Çeşidi",
        required=True,
        widget=ModelSelect2Widget(
            model=models.ProblemType,
            search_fields=["name__icontains"],
            max_results=100,
            attrs={
                "data-minimum-input-length": 0,
            }
        )
    )

    class Meta:
        model = models.Problem
        exclude = ["related_person", "is_approved", "related_district"]
        widgets = {
            # "thematic_field": Select2MultipleWidget
        }

# related_person_formset = inlineformset_factory(models.Person, models.Problem, form=RelatedPersonForm, extra=0)

class AddressForm(forms.Form):
    province = forms.ModelChoiceField(
        queryset=models.Province.objects.all(),
        label=u"İl",
        required=False,
        widget=ModelSelect2Widget(
            model=models.Province,
            search_fields=["name_1__icontains"],
            max_results=100,
            attrs = {
                "data-minimum-input-length": 0
            }
        )
    )
    district = forms.ModelChoiceField(
        queryset=models.District.objects.all(),
        label=u"İlçe",
        required=False,
        widget=ModelSelect2Widget(
            model=models.District,
            search_fields=["name_2__icontains"],
            dependent_fields={"province": "related_province"},
            max_results=500,
            attrs={
                "data-minimum-input-length": 0
            }
        )
    )
