from django.contrib import admin
from gofor_problem_map.problem_map import models
from django.db import models as django_models
from leaflet.admin import LeafletGeoAdminMixin
from django_reverse_admin import ReverseModelAdmin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from ckeditor.widgets import CKEditorWidget
from import_export import resources, fields, widgets
from import_export.admin import ImportExportMixin, ImportMixin
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

# DJANGO IMPORT EXPORT

class ProblemResource(resources.Resource):
    # pk = fields.Field("pk")
    # name = fields.Field("name")
    # description = fields.Field("description")
    # related_person = fields.Field(column_name="related_person",
    #                               attribute="related_person.first_name",
    #                               widget=widgets.ForeignKeyWidget((models.Person, "pk")))
    # occurrence_date = fields.Field(attribute="occurrence_date",
    #                                widget=widgets.DateWidget(format="%d-%m-%Y"))
    # related_district = fields.Field(column_name="related_district",
    #                                 attribute="related_district",
    #                                 widget=widgets.ForeignKeyWidget((models.District, "pk")))
    class Meta:
        model = models.Problem
        import_id_fields = "pk"
        fields = ("pk",
                  "name",
                  "description",
                  # "related_problem_type",
                  "occurrence_date",
                  "related_person__first_name",
                  "related_person__last_name",
                  "related_person__could_contact",
                  "related_person__email",
                  "related_person__phone_number",
                  "related_person__sex"
                  "related_district__name_1",)
        # export_order =
        skip_unchanged = False
        report_skipped = True


# class RelatedPersonInline(admin.TabularInline):
#     model = models.Person

class ProblemTypeAdmin(admin.ModelAdmin):
    model = models.ProblemType
    list_display = ["pk", "is_approved", "name","get_thematic_fields" , "created_at", "updated_at"]
    list_display_links = ["pk", "name"]
    list_editable = ["is_approved"]
    readonly_fields = ["created_at", "updated_at"]

    def get_thematic_fields(self, obj):
        return ", ".join([thematic_field.__str__() for thematic_field in obj.thematic_field.all()])

admin.site.register(models.ProblemType, ProblemTypeAdmin)


def make_published(modeladmin, request, queryset):
    queryset.update(is_approved=True)

class ProblemAdmin(ImportExportMixin, LeafletGeoAdminMixin, ReverseModelAdmin):
    model = models.Problem
    inline_type = 'stacked'
    inline_reverse = ["related_person"]
    actions = [make_published]
    list_display = ["pk", "is_approved", "related_person", "name", "created_at", "related_district", "related_problem_type"]
    list_display_links = ["pk", "name"]
    list_editable = ["is_approved"]
    date_hierarchy = "created_at"
    readonly_fields = ["created_at", "updated_at"]
    fields = (
        ("is_approved", "created_at", "updated_at"),
        ("name", "description"),
        "location",
        ("related_district", "related_problem_type"),
    )
    list_filter = ["is_approved",
                   "related_problem_type__thematic_field",
                   ("related_district__related_province", admin.RelatedOnlyFieldListFilter),
                   ]
    resource_class = ProblemResource


    # def get_thematic_fields(self, obj):
    #     return ", ".join([thematic_field.__str__() for thematic_field in obj.thematic_field.all()])

admin.site.register(models.Problem, ProblemAdmin)
admin.site.register(models.ThematicField)
class PersonAdmin(admin.ModelAdmin):
    model = models.Person
    list_display = ["pk", "first_name", "last_name","could_contact", "email", "phone_number"]

admin.site.register(models.Person, PersonAdmin)



# FLAT PAGES
# Define a new FlatPageAdmin

class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )
    formfield_overrides = {
        django_models.TextField: {"widget": CKEditorWidget},
    }


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
