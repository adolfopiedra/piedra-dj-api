from django.contrib.gis.geos import GEOSGeometry
 #to convert objects to dicts
from scripts.myLib.p1Settings import EPSG_CODE
from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Parks
from django.http import JsonResponse


class Parks_crud:
    def insert(self,dict):
        try:
            g = GEOSGeometry(dict['geom'], srid=EPSG_CODE)
            if not g.valid:
                d={'ok': False,
                'message': g.valid_reason,
                'data':None}
                print(d)
                return d
            print('Valid Geometry')

            b = Parks(description=dict["description"],
                    area=g.area,
                    type=dict["type"],
                    management=dict["management"],
                    equipment=dict["equipment"],
                    geom=g)

            b.save()

            d = {"ok": True,
                "message": "Data inserted",
                "data": [{"id": b.id}]}

            print(d)
            return d
        except Exception as e:
                d = {"ok": False,
                    "message": str(e),
                    "data": None}
                print(d)
                return d
        
    def update(self,dict):
        try:
            g = GEOSGeometry(dict['geom'], srid=EPSG_CODE)

            if not g.valid:
                d={'ok': False,
                'message': g.valid_reason,
                'data':None}
                print(d)
                return d

            print('Valid Geometry')

            p = Parks.objects.filter(id=dict['id']).first()

            if p:
                p.area = g.area
                p.description = dict['description']
                p.type = dict['type']
                p.management = dict['management']
                p.equipment = dict['equipment']
                p.geom = g
                p.save()

                d = {"ok": True,
                    "message": "Data updated",
                    "data": [{"rows_updated": 1}]}
            else:
                d = {"ok":False,
                    "message":"No row found with that id",
                    "data":None}
            print(d)
            return d
        except Exception as e:
                d = {"ok": False,
                    "message": str(e),
                    "data": None}
                print(d)
                return d
        
    def select(self,dict,asDict=False):
        return dbdj.select(self,Parks,dict,asDict)
    
    def selectallAsDicts(self):
        return dbdj.selectallAsDicts(self,Parks)
        
    def delete(self,dict):
        return dbdj.delete(self,Parks,dict)
