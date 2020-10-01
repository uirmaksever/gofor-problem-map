from django.db import models
from django.contrib.gis.db import models as gis_models
from djgeojson.fields import PointField
from django.urls import reverse
from django.shortcuts import redirect
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.db.models.signals import post_delete
# Create your models here.

DEFAULT_CHAR_LENGTH = 1024


class Country(gis_models.Model):
    id = gis_models.IntegerField(primary_key=True)
    gid_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    name_0 = gis_models.CharField(max_length=2048, null=True, blank=True)
    geom = gis_models.MultiPolygonField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.name_0

    class Meta:
        verbose_name = "Ülke"
        verbose_name_plural = "Ülkeler"


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

    class Meta:
        verbose_name = "İl"
        verbose_name_plural = "İller"


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

    class Meta:
        verbose_name = "İlçe"
        verbose_name_plural = "İlçeler"


class ThematicField(models.Model):
    name = models.CharField(max_length=DEFAULT_CHAR_LENGTH, verbose_name="Tematik Alan İsmi")
    description = RichTextField(null=True, blank=True, verbose_name="Açıklama")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tematik Alan"
        verbose_name_plural = "Tematik Alanlar"


class Person(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=DEFAULT_CHAR_LENGTH, verbose_name="İsim")
    last_name = models.CharField(max_length=DEFAULT_CHAR_LENGTH, verbose_name="Soyisim")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Adresi")
    could_contact = models.BooleanField(verbose_name="İletişim İzni")
    email = models.EmailField(null=True, blank=True, verbose_name="E-Posta Adresi")
    phone_number = PhoneNumberField(null=True, blank=True, verbose_name="Telefon No")
    birth_year = models.IntegerField(null=True, blank=True)
    sex = models.CharField(null=True, blank=True,
                           max_length=8)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    class Meta:
        verbose_name = "Kişi"
        verbose_name_plural = "Kişiler"


class ProblemType(models.Model):
    name = models.TextField(verbose_name="Problem Çeşidi Tanımı")
    thematic_field = models.ManyToManyField(ThematicField, verbose_name="Tematik Alan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    is_approved = models.BooleanField(default=False, verbose_name="Onay")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("problem_map:problemtype-detail", args=[str(self.pk)])

    @property
    def all_thematic_fields(self):
        return ", ".join([x.name for x in self.thematic_field.all()])

    class Meta:
        verbose_name = "Problem Çeşidi"
        verbose_name_plural = "Problem Çeşitleri"


class Problem(models.Model):
    name = models.CharField(max_length=1000, verbose_name="Problem Tanımı")
    description = models.TextField(verbose_name="Açıklama")
    related_problem_type = models.ForeignKey(ProblemType, on_delete=models.CASCADE, verbose_name="İlgili Problem Çeşidi")
    location = gis_models.PointField(verbose_name="Konum")
    occurrence_date = models.DateField(verbose_name="Gerçekleşme Tarihi")
    # thematic_field = models.ManyToManyField(ThematicField)
    related_person = models.OneToOneField(Person, on_delete=models.CASCADE, verbose_name="İlgili Kişi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    is_approved = models.BooleanField(default=False, verbose_name="Onay")
    related_district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="İlçe")

    def __str__(self):
        return "[{}] {} - {}".format(
            self.created_at.strftime("%d-%m-%Y %H:%M"),
            self.related_person,
            self.name
        )

    def get_absolute_url(self):
        return reverse("problem_map:problem-detail", args=[str(self.pk)])

    class Meta:
        verbose_name = "Problem"
        verbose_name_plural = "Problemler"

# SIGNALS
# When problem get deleted, related person is deleted as well
@receiver(post_delete, sender=Problem)
def problem_post_delete(sender, instance, *args, **kwargs):
    print("DELETED ", instance.related_person.pk)
    instance.related_person.delete()
