# myapp/wizard.py
import data_wizard
from . import models
from rest_framework import serializers

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = "__all__"

    data_wizard = {
        'header_row': 0,
        'start_row': 1,
        'show_in_list': True,
    }

data_wizard.register("Problem", ProblemSerializer)
