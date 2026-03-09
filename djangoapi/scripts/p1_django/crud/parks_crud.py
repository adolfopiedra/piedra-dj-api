from django.contrib.gis.geos import GEOSGeometry
from django.forms.models import model_to_dict #to convert objects to dicts
from valuableP1_v3.myLib.p1Settings import EPSG_CODE
from infraverde.models import Parks
from pprint import pprint
from django.http import JsonResponse

class Parks_crud:
    def insert(self,dict):
        g=GEOSGeometry(dict['geom'], srid=EPSG_CODE)
        if g.valid:
            print(g.valid_reason)
        else:
            d={'ok': False,
               'message':'Invalid geometry',
               'data':None}
            print(d)
            return d
        b=Parks(description=dict["description"],
                area=g.area,
                type=dict["type"],
                management = dict["management"],
                equipment = dict["equipment"],
                geom=g)
        b.save()
        d = {"ok": True,
            "message": "Data inserted",
            "data": [{"id": b.id}]}
        print(d)
        return d
    
    def update(self,dict):
        pass

    def select(self,dict,asDict=False):
        if asDict:
            filterById = Parks.objects.filter(id=dict['id'])
            l=list(filterById)
            b=l[0]
            d = {"ok": True,
                "message": "Data retrieved",
                "data": [model_to_dict(b)]}
            print(d)
            return d
        else:
            l = filterById = Parks.objects.filter(id=dict['id']).values_list()
            d={"ok": True,
                "message": "Data retrieved",
                "data": [l[0]]}
            print(d)
            return d

    def delete(self,dict):
        pass