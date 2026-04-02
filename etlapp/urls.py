from django.urls import path
from . import views

urlpatterns = [
    path("",         views.dashboard_view,  name="dashboard"),
    path("etl/",     views.upload_and_run,  name="etl"),
    path("results/", views.results_view,    name="results"),
]
