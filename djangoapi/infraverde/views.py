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

#To allow user autenticated
from django.contrib.auth.mixins import LoginRequiredMixin

class Infraverde01(View):
    def get(self, request):
        return JsonResponse({
            "ok": True,
            "message": "Infraverde. GET. Hello world",
            "data": [request.GET.dict()]
        }, status=200)

    def post(self, request):

        body_data = {}

        # Caso 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()

        # Caso 2: raw JSON
        else:
            try:
                body_data = json.loads(request.body.decode("utf-8"))
            except:
                body_data = {}

        return JsonResponse({
            "ok": True,
            "message": "Infraverde. POST. Hello world",
            "data": [body_data]
        }, status=200)

class Parks(LoginRequiredMixin, BaseDjangoView):
    #url login
    login_url = '/core/not_loggedin/'

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
        body_data = {}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        else:
            body_data=json.loads(request.body)

        equipment_raw = body_data.get('equipment', False)

        if equipment_raw in [True, 'true', 'True', 'TRUE', '1', 1]:
            body_data['equipment'] = True
        elif equipment_raw in [False, 'false', 'False', 'FALSE', '0', 0]:
            body_data['equipment'] = False
        else:
            body_data['equipment'] = None


        r = self.p.insert(body_data)
        return JsonResponse(r)
    
    def update(self, request, id):
        body_data = {}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        else:
            body_data=json.loads(request.body)

        equipment_raw = body_data.get('equipment', False)

        if equipment_raw in [True, 'true', 'True', 'TRUE', '1', 1]:
            body_data['equipment'] = True
        elif equipment_raw in [False, 'false', 'False', 'FALSE', '0', 0]:
            body_data['equipment'] = False
        else:
            body_data['equipment'] = None

        r = self.p.update(body_data)
        return JsonResponse(r)
    
    def delete(self, id):
        r = self.p.delete({'id': id})
        return JsonResponse(r)

class Corridors(LoginRequiredMixin, BaseDjangoView):
    #url login
    login_url = '/core/not_loggedin/'

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
        body_data = {}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        else:
            body_data=json.loads(request.body)

        lighting_raw = body_data.get('lighting', False)

        if lighting_raw in [True, 'true', 'True', 'TRUE', '1', 1]:
            body_data['lighting'] = True
        elif lighting_raw in [False, 'false', 'False', 'FALSE', '0', 0]:
            body_data['lighting'] = False
        else:
            body_data['lighting'] = None

        r = self.c.insert(body_data)
        return JsonResponse(r)
    
    def update(self, request, id):
        body_data = {}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        else:
            body_data=json.loads(request.body)

        lighting_raw = body_data.get('lighting', False)

        if lighting_raw in [True, 'true', 'True', 'TRUE', '1', 1]:
            body_data['lighting'] = True
        elif lighting_raw in [False, 'false', 'False', 'FALSE', '0', 0]:
            body_data['lighting'] = False
        else:
            body_data['lighting'] = None

        r = self.c.update(body_data)
        return JsonResponse(r)
    
    def delete(self, id):
        r = self.c.delete({'id': id})
        return JsonResponse(r)

class Trees(LoginRequiredMixin, BaseDjangoView):
    #url login
    login_url = '/core/not_loggedin/'
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
        body_data = {}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        else:
            body_data=json.loads(request.body)
        
        is_protected_raw = body_data.get('is_protected', False)

        if is_protected_raw in [True, 'true', 'True', 'TRUE', '1', 1]:
            body_data['is_protected'] = True
        elif is_protected_raw in [False, 'false', 'False', 'FALSE', '0', 0]:
            body_data['is_protected'] = False
        else:
            body_data['is_protected'] = None

        r = self.c.insert(body_data)
        return JsonResponse(r)
    
    def update(self, request, id):
        body_data = {}
        #CASO 1: form-data o x-www-form-urlencoded
        if request.POST:
            body_data = request.POST.dict()
        #CASO 2: raw json
        else:
            body_data=json.loads(request.body)

        is_protected_raw = body_data.get('is_protected', False)

        if is_protected_raw in [True, 'true', 'True', 'TRUE', '1', 1]:
            body_data['is_protected'] = True
        elif is_protected_raw in [False, 'false', 'False', 'FALSE', '0', 0]:
            body_data['is_protected'] = False
        else:
            body_data['is_protected'] = None

        r = self.c.update(body_data)
        return JsonResponse(r)
    
    def delete(self, id):
        r = self.c.delete({'id': id})
        return JsonResponse(r)

