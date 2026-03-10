from django.contrib.gis.geos import GEOSGeometry
 #to convert objects to dicts
from scripts.myLib.p1Settings import EPSG_CODE
from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Trees
from django.http import JsonResponse


class Trees_crud:
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

            b = Trees(description=dict["description"],
                    species=dict["species"],
                    height=dict["height"],
                    condition=dict["condition"],
                    is_protected=dict["is_protected"],
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

            p = Trees.objects.filter(id=dict['id']).first()

            if p:
                p.description = dict['description']
                p.species = dict['species']
                p.height = dict['height']
                p.condition = dict['condition']
                p.is_protected = dict['is_protected']
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
        return dbdj.select(self,Trees,dict,asDict)
    
    def selectallAsDicts(self):
        return dbdj.selectallAsDicts(self,Trees)
        
    def delete(self,dict):
        return dbdj.delete(self,Trees,dict)
