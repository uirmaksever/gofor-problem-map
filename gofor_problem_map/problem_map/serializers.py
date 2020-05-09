from rest_framework import serializers
from . import models
# from rest_framework_gis.serializers import GeoFeatureModelSerializer
from djgeojson.serializers import Serializer as DJGeojsonSerializer

class ProblemSerializer(serializers.ModelSerializer):
    # That's how you can avoid depth for certain fields
    related_district = serializers.CharField(source="related_district.__str__", read_only=True)
    class Meta:
        model = models.Problem
        fields = ("pk", "name", "description", "location", "related_problem_type", "related_person", "created_at", "related_district")
        depth = 1
        read_only_fields = ("pk", "name", "description", "location", "related_problem_type", "related_person", "created_at", "related_district")


class ThematicFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThematicField
        fields = "__all__"
        read_only_fields = ("name",)
