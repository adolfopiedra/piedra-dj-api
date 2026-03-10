from django.contrib.gis.geos import GEOSGeometry
 #to convert objects to dicts
from scripts.myLib.p1Settings import EPSG_CODE
from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Corridors
from django.http import JsonResponse

class Corridors_crud:
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

            b = Corridors(description=dict["description"],
                        dist=g.length,
                        type=dict["type"],
                        width=dict["width"],
                        lighting=dict["lighting"],
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

            p = Corridors.objects.filter(id=dict['id']).first()

            if p:
                p.description = dict['description']
                p.dist = g.length
                p.type = dict['type']
                p.width = dict['width']
                p.lighting = dict['lighting']
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
        return dbdj.select(self,Corridors,dict,asDict)
    
    def selectallAsDicts(self):
        return dbdj.selectallAsDicts(self,Corridors)
        
    def delete(self,dict):
        return dbdj.delete(self,Corridors,dict)
