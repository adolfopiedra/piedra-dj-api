from django.urls import path
from . import views

urlpatterns = [
    path("hello_infraverde/", views.Infraverde01.as_view(),name="infraverde"),
    path("parks/", views.Parks.as_view(),name="parks")
]