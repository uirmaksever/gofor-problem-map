from django import forms
from leaflet.forms.fields import PointField
from leaflet.forms.widgets import LeafletWidget
from . import models
from django.forms.models import inlineformset_factory
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget, Select2MultipleWidget
from bootstrap_datepicker_plus import DatePickerInput
from phonenumber_field.formfields import PhoneNumberField
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3, ReCaptchaV2Checkbox

class CustomMapWidget(LeafletWidget):
    template_name = "problem_map/custom_map_widget.html"

class RelatedPersonForm(forms.ModelForm):
    first_name = forms.CharField(label="İsminiz",
                                 widget=forms.TextInput(attrs={"placeholder": "Barış"}))
    last_name = forms.CharField(label="Soyisminiz",
                                widget=forms.TextInput(attrs={"placeholder": "Manço"}))
    could_contact = forms.BooleanField(label="Sizinle iletişim kurabilir miyiz?",
                                       required=False,
                                       help_text="""Probleminizle ilgili gelişmeleri sizle paylaşabiliriz. Bunun için iletişim
                                                 bilgilerinizi bizle paylaşmalısınız. İsim soyisminiz ve iletişim bilgileriniz
                                                 sitede görüntülenmeyecek, izniniz olmadan ilgili kurum ya da kişilerle
                                                 paylaşılmayacaktır. Probleminizi anonim olarak paylaşmak isterseniz
                                                 iletişim bilgilerinizi boş bırakabilirsiniz.""",
                                       )
    email = forms.EmailField(label="E-Posta adresiniz",
                             required=False,
                             widget=forms.EmailInput(attrs={"placeholder": "lukeskywalker@jedi.org"}))
    phone_number = PhoneNumberField(label="Telefon numaranız",
                                    required=False,
                                    help_text="""Telefon numaranız Türkiye içinde kullanılır bir telefon numarası olmalıdır.
                                              Geçerli telefon numarası 5071234567, 05071234567, +905071234567 şeklinde olabilir.
                                              """,)

    class Meta:
        model = models.Person
        exclude = ["ip"]

class ProblemTypeForm(forms.ModelForm):
    name = forms.CharField(label="Problem Tanımlamanız",
                           widget=forms.TextInput(attrs={"placeholder": "Ör: İşten Çıkarılma"}))
    captcha = ReCaptchaField(widget=ReCaptchaV3)
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
                "placeholder": "Ör: İşten çıkarıldım."
            }
        )
    )

    class Meta:
        model = models.ProblemType
        fields = ["name", "thematic_field"]



class ProblemForm(forms.ModelForm):
    name = forms.CharField(label="Problem başlığı",
                           help_text="Probleminizi üç beş kelime ile kısaca özetleyin.",
                           widget=forms.TextInput(attrs={"placeholder": "Ör: Ben ve çalışma arkadaşlarım işten çıkarıldık.",},
                                                  )
                           )
    description = forms.CharField(max_length=None,
                                  label="Problem detayları",
                                  help_text="""Probleminize ilişkin detayları özetleyin. Nasıl gerçekleştiğini,
                                    ne şekilde bir hak ihlaline uğradığınızı kısaca anlatın.""",
                                  widget=forms.TextInput(attrs={"placeholder": """Ör: Bir AVM'de reyon görevlisi olarak çalışıyorum. Korona salgını başladıktan sonra mağaza beni ve dört arkadaşımı işten çıkarttı ancak bu işten çıkarma yasağının yürürlüğe girmesinden önceydi. Maddi zorluk yaşamamıza rağmen tazminatlarımız hala ödenmedi. Özlük haklarımız ihlal edildi.""", },
                                                         )
                                  )
    location = PointField(required=False,
                          widget=CustomMapWidget,
                          label="Konum",
                          help_text="""Problemin gerçekleştiği konumu haritadan işaretleyin. Problem şu an bulunduğunuz yerde
                            gerçekleştiyse "Konumumu kullan" butonuna tıklayarak şu an bulunduğunuz yeri seçebilirsiniz.
                            Probleminiz kesin bir konumla ilgili değilse ya da kesin bir konum paylaşmak istemiyorsanız
                            "İl/ilçe seçmek istiyorum" seçeneğini kullanarak en az ilçe seviyesinde konum bilgisi paylaşınız.
                             (Sadece il seçemezsiniz.)""")
    occurrence_date = forms.DateField(widget=DatePickerInput(format="%d-%m-%Y", attrs={"placeholder": "Ör: 10-04-2020"}),
                                      label="Problemin gerçekleştiği tarih",
                                      help_text="Problemin gerçekeleştiği gerçek tarihi GG-AA-YYYY formatında yazın.")
    related_problem_type = forms.ModelChoiceField(
            queryset=models.ProblemType.objects.filter(is_approved=True),
            label="Problem Çeşidi",
            help_text="""Probleminizi en iyi şekilde tanımlayan seçeneği seçin. Bu seçimi yapmanız bizim istatistikleri daha"
                      sağlıklı tutmamızı, ilgili kurumlarla daha hızlı iletişime geçmemizi sağlayacak. Eğer yaşadığınız problem
                      listedekilerin hiçbirine benzemiyorsa aşağıdaki linke tıklayarak bize önerebilirsiniz. Halihazırda
                      girdiğiniz problem için problem çeşidini "Diğer" seçeneğini seçerek bizi gönderin, problem çeşidi önerinizi
                      değerlendirdikten sonra probleminizi biz kategorileyeceğiz.""",
            required=True,
            widget=ModelSelect2Widget(
                model=models.ProblemType,
                search_fields=["name__icontains"],
                max_results=100,
                attrs={
                    "data-minimum-input-length": 0,
                    "placeholder": "İşten çıkarıldım."
                }
            )
        )
    class Meta:
        model = models.Problem
        # exclude = ["related_person", "is_approved", "related_district"]
        fields = ["name", "description", "location", "occurrence_date", "related_problem_type"]
        widgets = {
            # "thematic_field": Select2MultipleWidget
        }

# related_person_formset = inlineformset_factory(models.Person, models.Problem, form=RelatedPersonForm, extra=0)

class AddressForm(forms.Form):
    province = forms.ModelChoiceField(
        queryset=models.Province.objects.all(),
        label=u"İl",
        help_text="Sadece il seçemezsiniz",
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
