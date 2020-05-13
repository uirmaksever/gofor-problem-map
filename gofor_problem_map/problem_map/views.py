from django.shortcuts import render, redirect
from gofor_problem_map.dash import example_dash, plotly_offline_example, districts_plotly
from rest_framework import viewsets
from . import models
from . import forms
from . import serializers
from django.views.generic import CreateView, DetailView, ListView
from extra_views import CreateWithInlinesView, InlineFormSetFactory
import django.contrib.messages as messages
from ipware import get_client_ip
from django_filters import rest_framework as filters
from gofor_problem_map.utils import helpers
from django_tables2 import tables, LinkColumn
# Create your views here.

def dash_example_view(request, template_name="dash/example_dash.html", **kwargs):
    'Example view that inserts content into the dash context passed to the dash application'

    context = {}

    # create some context to send over to Dash:
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['django_to_dash_context'] = "I am Dash receiving context from Django"
    request.session['django_plotly_dash'] = dash_context

    # Add ofline plotly graph to context
    context["plotly_graph"] = plotly_offline_example.scatter()
    context["districts_plotly"] = districts_plotly.render_map()
    return render(request, template_name=template_name, context=context)

# Added as a note for districts gadm file mapping to geodjango. Have no effect
mapping = {
    "name": "NAME_2",
    "province": "NAME_1",
    "poly": "MULTIPOLYGON"
}

class ThematicFieldViewSet(viewsets.ModelViewSet):
    queryset = models.ThematicField.objects.all()
    serializer_class = serializers.ThematicFieldSerializer

class ProblemsViewSet(viewsets.ModelViewSet):
    queryset = models.Problem.objects.filter(is_approved=True).order_by("-created_at")
    serializer_class = serializers.ProblemSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        # Any change made above reflected here
        queryset = self.queryset
        thematic_field = self.request.query_params.get("thematic_field", None)
        if thematic_field == "all":
            queryset = queryset
        elif thematic_field is not None:
            queryset = queryset.filter(related_problem_type__thematic_field=thematic_field)
        return queryset

class ProblemDetailView(DetailView):
    model = models.Problem

    def get_context_data(self, **kwargs):
        context = super(ProblemDetailView, self).get_context_data(**kwargs)
        object = self.get_object()

        return context


class RelatedProblemsTable(tables.Table):
    name = LinkColumn()

    class Meta:
        model = models.Problem
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "created_at", "related_district")

class ThematicDetailView(DetailView):
    model = models.ThematicField

    def get_context_data(self, **kwargs):
        context = super(ThematicDetailView, self).get_context_data(**kwargs)
        object = self.get_object()
        print(object.pk)
        context["problems"] = models.Problem.objects.filter(related_problem_type__thematic_field=object)
        context["problems_table"] = RelatedProblemsTable(data=context["problems"])
        return context

class ProblemTypeDetailView(DetailView):
    model = models.ProblemType
    # Using the same template with Thematic Field Detail View
    template_name = "problem_map/thematicfield_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProblemTypeDetailView, self).get_context_data(**kwargs)
        object = self.get_object()
        print(object.pk)
        context["problems"] = models.Problem.objects.filter(related_problem_type=object)
        context["problems_table"] = RelatedProblemsTable(data=context["problems"])
        return context
class ThematicListView(ListView):
    model = models.ThematicField

class ProblemTypeCreateView(CreateView):
    model = models.ProblemType
    form_class = forms.ProblemTypeForm

class ProblemCreateView(CreateView):
    model = models.Problem
    person_form_class = forms.RelatedPersonForm
    form_class = forms.ProblemForm

    def get_context_data(self, **kwargs):
        context = super(ProblemCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["form"] = self.form_class(self.request.POST)
            context["related_person_form"] = self.person_form_class(self.request.POST)
            context["address_form"] = forms.AddressForm(self.request.POST)
        else:
            context["form"] = self.form_class()
            context["related_person_form"] = self.person_form_class()
            context["address_form"] = forms.AddressForm()
        return context

    def form_valid(self, form):
        context = self.request.POST
        form = self.form_class(context)
        related_person_form = self.person_form_class(context)
        address_form = forms.AddressForm(context)
        forms_dict = {"form": form,
                      "related_person_form": related_person_form,
                      "address_form": address_form}

        custom_validations = True
        if form.is_valid():
            # LOCATION & PROVINCE/DISTRICT VALIDATIONS
            # Check if user either selected location or province/district
            if form.has_changed():
                if not "location" in form.changed_data and not address_form.has_changed():
                    messages.add_message(self.request, messages.ERROR,
                                         """Ya haritadan konum eklemeli ya da il/ilçe seçmelisiniz.""")
                    custom_validations = False

            # Check if user user both selected exact location and province/district
            if form.has_changed():
                if "location" in form.changed_data and address_form.has_changed():
                    messages.add_message(self.request, messages.ERROR,
                                         """Hem haritadan konum seçtiniz, hem de il/ilçe seçtiniz. Lütfen sadece birini seçin.""")
                    custom_validations = False

            if address_form.is_valid():
                # Check user also selected a district
                if address_form.has_changed() and not "district" in address_form.changed_data:
                    messages.add_message(self.request, messages.ERROR,
                                         """Sadece il seçtiniz. Lütfen ilçe de seçin. İsterseniz merkez ilçe seçebilirsiniz.""")
                    custom_validations = False

                # RELATED PERSON VALIDATIONS
                if related_person_form.is_valid() is False:
                    messages.add_message(self.request, messages.ERROR, "Kişi ile ilgili detaylarda yanlışlık var.")
                    custom_validations = False

                if custom_validations is False:
                    return render(self.request, self.get_template_names(), forms_dict)

                # Check if user selected province/district instead of exact location
                if address_form.has_changed():
                    related_district = address_form.cleaned_data["district"]
                    # If district is selected, make location selected district's centroid
                    form.instance.location = related_district.geom.centroid
                    print(related_district.geom.centroid)

                # Checking for custom validations twice due to location assignment
                if custom_validations is False:
                    return render(self.request, self.get_template_names(), forms_dict)


            # Check if selected location is in Turkey
            is_in_turkey = helpers.is_in_turkey(form.instance.location)
            if is_in_turkey is False:
                messages.add_message(self.request, messages.ERROR,
                                     """Seçtiğiniz konum Türkiye dışında bulunmaktadır.
                                     Lütfen Türkiye içinde bir konum seçiniz.""")
                print(self.get_template_names())
                custom_validations = False




            if related_person_form.is_valid():
                # Get user's IP address
                client_ip, is_routable = get_client_ip(self.request)
                print(client_ip)
                related_person_form.save(commit=False)
                related_person_form.instance.ip = client_ip

                # Finally, save related person
                related_person_form.save()

            # Get district of the location
            related_district = helpers.find_district(point=form.instance.location)
            form.instance.related_district = related_district
            form.instance.related_person = related_person_form.instance

            messages.add_message(self.request, messages.SUCCESS,
                                 """
                                 Paylaştığınız için teşekkürler! Probleminiz başarıyla bize iletildi.
                                 Onaylandıktan sonra web sitesinde görüntülenecektir.
                                 """)
        return super(ProblemCreateView, self).form_valid(form)


    def post(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()

        return super(ProblemCreateView, self).post(request, *args, **kwargs)

def send_test_email(request):
    from django.core.mail import send_mail

    send_mail("Subject", "text body", "covid@go-for.org",
              ["umutirmaksever@gmail.com"])

    messages.success(request=request, message="Test maili gönderildi")
    return redirect("map")
