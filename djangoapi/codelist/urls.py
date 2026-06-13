from django.urls import path
from codelist import views
urlpatterns = [
    path("hello_world/", views.HelloWord.as_view(),name="hello_world"),
    path('park-types/selectall/', views.park_types_selectall),
    path('park-managements/selectall/', views.park_managements_selectall),
    path('corridor-types/selectall/', views.corridor_types_selectall),
    path('tree-species/selectall/', views.tree_species_selectall),
    path('tree-conditions/selectall/', views.tree_conditions_selectall),
]