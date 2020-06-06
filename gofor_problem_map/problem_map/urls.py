from django.urls import path, include
from . import views
from . import models
from rest_framework import routers
from djgeojson.views import GeoJSONLayerView

app_name = "problem_map"

router = routers.DefaultRouter()
router.register(r'problems', views.ProblemsViewSet)
router.register(r'thematic_fields', views.ThematicFieldViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("data.geojson", GeoJSONLayerView.as_view(model=models.Problem, geometry_field="location", properties=("name","pk")), name="data"),
    path("create", views.ProblemCreateView.as_view(), name="problem-create"),
    path("problem/<int:pk>", views.ProblemDetailView.as_view(), name="problem-detail"),
    path("thematic/<int:pk>", views.ThematicDetailView.as_view(), name="thematic-detail"),
    path("thematic/", views.ThematicListView.as_view(), name="thematic-list"),
    path("suggest_problem_type/", views.ProblemTypeCreateView.as_view(), name="problem-type-suggest"),
    path("suggest_problem_type_modal/", views.ProblemTypeModalCreateView.as_view(), name="problem-type-suggest-modal"),
    path("problem_type/<int:pk>", views.ProblemTypeDetailView.as_view(), name="problemtype-detail"),
    path("send_test_email", views.send_test_email, name="send_test_email")

]
