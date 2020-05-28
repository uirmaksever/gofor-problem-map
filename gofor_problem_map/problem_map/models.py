from django.db import models
from django.contrib.gis.db import models as gis_models
from djgeojson.fields import PointField
from django.urls import reverse
from django.shortcuts import redirect
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
# Create your models here.

DEFAULT_CHAR_LENGTH = 1024


class Country(gis_models.Model):
    id = gis_models.IntegerField(primary_key=True)
    gid_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    name_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    geom = gis_models.MultiPolygonField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.name_0


class Province(gis_models.Model):
    id = gis_models.IntegerField(primary_key=True)
    gid_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    name_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    gid_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    name_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    varname_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    nl_name_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    type_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    engtype_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    cc_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    hasc_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    geom = gis_models.MultiPolygonField(srid=4326, null=True, blank=True)
    related_country = gis_models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_1


class District(gis_models.Model):
    id = gis_models.IntegerField(primary_key=True)
    gid_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    name_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    gid_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    name_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    nl_name_1 = gis_models.CharField(max_length=2048, null=True, blank=True)
    gid_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    name_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    varname_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    nl_name_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    type_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    engtype_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    cc_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    hasc_2 = gis_models.CharField(max_length=2048, null=True, blank=True)
    geom = gis_models.MultiPolygonField(srid=4326, null=True, blank=True)
    related_province = gis_models.ForeignKey(Province, on_delete=gis_models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.name_1, self.name_2)






class ThematicField(models.Model):
    name = models.CharField(max_length=DEFAULT_CHAR_LENGTH)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    first_name = models.CharField(max_length=DEFAULT_CHAR_LENGTH)
    last_name = models.CharField(max_length=DEFAULT_CHAR_LENGTH)
    ip = models.GenericIPAddressField(null=True, blank=True)
    could_contact = models.BooleanField()
    email = models.EmailField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class ProblemType(models.Model):
    name = models.TextField()
    thematic_field = models.ManyToManyField(ThematicField)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("problem_map:problemtype-detail", args=[str(self.pk)])

class Problem(models.Model):
    name = models.CharField(max_length=1000)
    description = models.TextField()
    related_problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE)
    location = gis_models.PointField()
    occurrence_date = models.DateField()
    # thematic_field = models.ManyToManyField(ThematicField)
    related_person = models.OneToOneField(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    related_district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return "[{}] {} - {}".format(
            self.created_at.strftime("%d-%m-%Y %H:%M"),
            self.related_person,
            self.name
        )

    def get_absolute_url(self):
        return reverse("problem_map:problem-detail", args=[str(self.pk)])

