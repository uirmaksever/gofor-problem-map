from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import viewsets
from gofor_problem_map.problem_map import models
from gofor_problem_map.problem_map import forms
from gofor_problem_map.problem_map import serializers
from django.views.generic import CreateView, DetailView, ListView
from extra_views import CreateWithInlinesView, InlineFormSetFactory
import django.contrib.messages as messages
from ipware import get_client_ip
from django_filters import rest_framework as filters
from gofor_problem_map.utils import helpers
from django_tables2 import tables, LinkColumn
from django.contrib.messages.views import SuccessMessageMixin
from bootstrap_modal_forms.generic import BSModalCreateView

# Create your views here.


class ThematicFieldViewSet(viewsets.ModelViewSet):
    queryset = models.ThematicField.objects.all()
    serializer_class = serializers.ThematicFieldSerializer

class ProblemsViewSet(viewsets.ModelViewSet):
    queryset = models.Problem.objects.filter(is_approved=True).order_by("-created_at")
    serializer_class = serializers.ProblemSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def get_queryset(self):
        # Any change made above reflected here
        queryset = models.Problem.objects.filter(is_approved=True).order_by("-created_at")
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
        context["problems"] = models.Problem.objects.filter(related_problem_type__thematic_field=object,
                                                            is_approved=True)
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
        context["problems"] = models.Problem.objects.filter(related_problem_type=object,
                                                            is_approved=True)
        context["problems_table"] = RelatedProblemsTable(data=context["problems"])
        return context

class ThematicListView(ListView):
    model = models.ThematicField

class ProblemTypeCreateView(SuccessMessageMixin, CreateView):
    model = models.ProblemType
    form_class = forms.ProblemTypeForm
    success_message = "Problem çeşidi önerinizi başarıyla aldık. Gözden geçirdikten sonra listemize ekleyeceğiz. Teşekkürler!"

class ProblemTypeModalCreateView(BSModalCreateView):
    template_name = "problem_map/problemtype_modalform.html"
    form_class = forms.ProblemTypeBSForm
    success_message = """Teşekkürler! Problem çeşidi önerinizi başarıyla aldık. Gözden geçirdikten sonra listemize ekleyeceğiz.
                        Lütfen probleminizin kalan detaylarını da doldurmayı unutmayın.
                      """
    success_url = reverse_lazy("problem_map:problem-create")

class ProblemCreateView(SuccessMessageMixin, CreateView):
    model = models.Problem
    person_form_class = forms.RelatedPersonForm
    form_class = forms.ProblemForm
    success_message = """Paylaştığınız için teşekkürler! Probleminiz başarıyla bize iletildi.
    Onaylandıktan sonra web sitesinde görüntülenecektir."""

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

            # Get district of the location
            related_district = helpers.find_district(point=form.instance.location)
            print(related_district)
            if related_district is not None:
                form.instance.related_district = related_district
            else:
                messages.add_message(self.request, messages.ERROR,
                                     """Haritadan seçtiğiniz konum için geçerli bir yerleşim birimi bulamadık. Lütfen
                                     girdiğiniz konumun Türkiye içinde olduğundan emin olun ya da il/ilçe seçin.""")
                return render(self.request, self.get_template_names(), forms_dict)
            # Related person
            if related_person_form.is_valid():
                # Get user's IP address
                client_ip, is_routable = get_client_ip(self.request)
                related_person_form.save(commit=False)
                related_person_form.instance.ip = client_ip

                # Finally, save related person
                related_person_form.save()
            # Assign newly saved related person to problem instance
            form.instance.related_person = related_person_form.instance


        else:
            return render(self.request, self.get_template_names(), forms_dict)

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

def view_queryset(request):
    qs = models.Problem.objects.values(
        "pk",
        "name",
        "description",
        "occurrence_date",
        "created_at",
        "updated_at",
        "is_approved",
        "related_problem_type__name",
        "related_problem_type__thematic_field__name",
        "related_person__first_name",
        "related_person__last_name",
        "related_person__could_contact",
        "related_person__email",
        "related_person__phone_number",
        "related_district__name_1",
        "related_district__name_2",
    )
    print(qs.query)
    context = {"qs": qs}
    return render(request, "problem_map/view_queryset.html", context)
