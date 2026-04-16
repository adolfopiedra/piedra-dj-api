from django.shortcuts import render

# Create your views here.
# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View

#My imports
from core.myLib.geometryTools import WkbConversor, GeometryChecks
from core.myLib.baseDjangoView import BaseDjangoView

#My code
#from 

class Infraverde01(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Infraverde. Hello world", "data":[request.GET.dict()]},status=200)
    def post(self, request):
        return JsonResponse({"ok":True,"message": "Infraverde. Hello world", "data":[request.POST.dict()]},status=200)

class Parks(BaseDjangoView):
    def post(self, request):
        d=request.POST.dict()
        return JsonResponse({"ok":True,"message": "Datos Recibidos en Parks (post)", "data":[request.POST.dict()]},status=200)

    def get(self, request):
        return JsonResponse({"ok":True,"message": "Datos Recibidos en Parks (get)", "data":[request.GET.dict()]},status=200)

class Trees(BaseDjangoView):
    pass

class Corridors(BaseDjangoView):
    pass

