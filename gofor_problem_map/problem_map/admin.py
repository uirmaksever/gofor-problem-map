from django.contrib import admin
from . import models
from leaflet.admin import LeafletGeoAdminMixin
from django_reverse_admin import ReverseModelAdmin

# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    list_display = ["__str__"]

admin.site.register(models.Country, CountryAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["__str__",]

admin.site.register(models.District, DistrictAdmin)

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["__str__"]

admin.site.register(models.Province, ProvinceAdmin)

# class RelatedPersonInline(admin.TabularInline):
#     model = models.Person

class ProblemTypeAdmin(admin.ModelAdmin):
    model = models.ProblemType
    list_display = ["pk", "name","get_thematic_fields" , "created_at", "updated_at"]
    list_display_links = ["pk", "name"]
    readonly_fields = ["created_at", "updated_at"]

    def get_thematic_fields(self, obj):
        return ", ".join([thematic_field.__str__() for thematic_field in obj.thematic_field.all()])

admin.site.register(models.ProblemType, ProblemTypeAdmin)


def make_published(modeladmin, request, queryset):
    queryset.update(is_approved=True)

class ProblemAdmin(LeafletGeoAdminMixin, ReverseModelAdmin):
    model = models.Problem
    inline_type = 'stacked'
    inline_reverse = ["related_person"]
    actions = [make_published]
    list_display = ["pk", "is_approved", "related_person", "name", "created_at", "related_district"]
    list_display_links = ["pk", "name"]
    list_editable = ["is_approved"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]
    fields = (
        ("is_approved", "created_at", "updated_at"),
        ("name", "description"),
        "location",
        ("thematic_field", "related_district"),
    )
    list_filter = ["is_approved",
                   "related_problem_type__thematic_field",
                   ("related_district__related_province", admin.RelatedOnlyFieldListFilter),
                   ]


    # def get_thematic_fields(self, obj):
    #     return ", ".join([thematic_field.__str__() for thematic_field in obj.thematic_field.all()])

admin.site.register(models.Problem, ProblemAdmin)
admin.site.register(models.ThematicField)
admin.site.register(models.Person)
