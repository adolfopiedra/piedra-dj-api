from django.shortcuts import render

# Create your views here.
# Create your views here.
#Django imports
from django.http import JsonResponse
from django.views import View

#My imports
from core.myLib.geometryTools import WkbConversor, GeometryChecks
from core.myLib.baseDjangoView import BaseDjangoView
import json
#My code
from infraverde.CRUD.parks.parks_crud import Parks_crud
from infraverde.CRUD.corridors.corridors_crud import Corridors_crud
from infraverde.CRUD.trees.trees_crud import Trees_crud

class Infraverde01(View):
    def get(self, request):
        return JsonResponse({"ok":True,"message": "Infraverde. Hello world", "data":[request.GET.dict()]},status=200)
    def post(self, request):
        return JsonResponse({"ok":True,"message": "Infraverde. Hello world", "data":[request.POST.dict()]},status=200)

class Parks(BaseDjangoView):
    #Constructor
    def __init__(self):
        self.p=Parks_crud()

    #GET OPERATIONS
    def selectone(self, id):
        r = self.p.select({'id': id},asDict=True)
        return JsonResponse(r)

    def selectall(self):
        r = self.p.selectallAsDicts()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        dict = json.loads(request.body)
        r = self.p.insert(dict)
        return JsonResponse(r)
    
    def update(self, request, id):
        dict = json.loads(request.body)
        r = self.p.update(dict)
        return JsonResponse(r)
    
    def delete(self, id):
        r = self.p.delete({'id': id})
        return JsonResponse(r)

class Corridors(BaseDjangoView):
    #Constructor
    def __init__(self):
        self.c=Corridors_crud()

    #GET OPERATIONS
    def selectone(self, id):
        r = self.c.select({'id': id},asDict=True)
        return JsonResponse(r)

    def selectall(self):
        r = self.c.selectallAsDicts()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        dict = json.loads(request.body)
        r = self.c.insert(dict)
        return JsonResponse(r)
    
    def update(self, request, id):
        dict = json.loads(request.body)
        r = self.c.update(dict)
        return JsonResponse(r)
    
    def delete(self, id):
        r = self.c.delete({'id': id})
        return JsonResponse(r)

class Trees(BaseDjangoView):
    #Constructor
    def __init__(self):
        self.c=Trees_crud()

    #GET OPERATIONS
    def selectone(self, id):
        r = self.c.select({'id': id},asDict=True)
        return JsonResponse(r)

    def selectall(self):
        r = self.c.selectallAsDicts()
        return JsonResponse(r)

    #POST OPERATIONS
    def insert(self, request):
        dict = json.loads(request.body)
        r = self.c.insert(dict)
        return JsonResponse(r)
    
    def update(self, request, id):
        dict = json.loads(request.body)
        r = self.c.update(dict)
        return JsonResponse(r)
    
    def delete(self, id):
        r = self.c.delete({'id': id})
        return JsonResponse(r)

