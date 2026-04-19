from django.urls import path
from . import views

urlpatterns = [
    path("hello_infraverde/", views.Infraverde01.as_view(),name="infraverde"),
    # urls for parks
    path('parks/<str:action>/', views.Parks.as_view(), name='parks'),  # POST requests
    path('parks/<str:action>/<int:id>/', views.Parks.as_view(), name='parks'),  # GET requests
    # urls for corridors
    path('corridors/<str:action>/', views.Corridors.as_view(), name='corridors'),  # POST requests
    path('corridors/<str:action>/<int:id>/', views.Corridors.as_view(), name='corridors'),  # GET requests
    # urls for trees
    path('trees/<str:action>/', views.Trees.as_view(), name='trees'),  # POST requests
    path('trees/<str:action>/<int:id>/', views.Trees.as_view(), name='trees'),  # GET requests
]