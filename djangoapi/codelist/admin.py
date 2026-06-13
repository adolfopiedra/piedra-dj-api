from django.contrib import admin
from .models import ParkType, ParkManagement, CorridorType, TreeSpecies, TreeCondition


admin.site.register(ParkType)
admin.site.register(ParkManagement)
admin.site.register(CorridorType)
admin.site.register(TreeSpecies)
admin.site.register(TreeCondition)