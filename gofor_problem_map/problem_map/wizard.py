# myapp/wizard.py
import data_wizard
from . import models
from rest_framework import serializers

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ["name",
                  "description",
                  "related_problem_type",
                  "occurrence_date",
                  "related_person__first_name",
                  "related_person__last_name",
                  "related_person__email",
                  "related_person__phone_number",
                  "related_person__sex",
                  "related_district"]

    data_wizard = {
        'header_row': 0,
        'start_row': 1,
        'show_in_list': True,
    }

data_wizard.register("Problem", ProblemSerializer)
