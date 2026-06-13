#Django imports
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import (
    ParkType,
    ParkManagement,
    CorridorType,
    TreeSpecies,
    TreeCondition
)

class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Codelist. Hello world", "data":[]})
    
login_url = '/core/not_loggedin/'

def park_types_selectall(request):
    data = list(ParkType.objects.values('id', 'name'))

    return JsonResponse({
        'ok': True,
        'message': 'Park types retrieved correctly',
        'data': data
    })


def park_managements_selectall(request):
    data = list(ParkManagement.objects.values('id', 'name'))

    return JsonResponse({
        'ok': True,
        'message': 'Park managements retrieved correctly',
        'data': data
    })


def corridor_types_selectall(request):
    data = list(CorridorType.objects.values('id', 'name'))

    return JsonResponse({
        'ok': True,
        'message': 'Corridor types retrieved correctly',
        'data': data
    })


def tree_species_selectall(request):
    data = list(TreeSpecies.objects.values('id', 'name'))

    return JsonResponse({
        'ok': True,
        'message': 'Tree species retrieved correctly',
        'data': data
    })


def tree_conditions_selectall(request):
    data = list(TreeCondition.objects.values('id', 'name'))

    return JsonResponse({
        'ok': True,
        'message': 'Tree conditions retrieved correctly',
        'data': data
    })