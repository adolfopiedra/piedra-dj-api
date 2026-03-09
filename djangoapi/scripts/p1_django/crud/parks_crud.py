from django.contrib.gis.geos import GEOSGeometry
from valuableP1_v3.myLib.p1Settings import EPSG_CODE
from infraverde.models import Parks

class Parks_crud:
    def insert(self,dict):
        g=GEOSGeometry(dict['geom'], srid=EPSG_CODE)
        if g.valid:
            print("Geometría válida")
        else:
            return {'ok': False, 'message':'Invalid geometry', 'data':None}
        b=Parks(description=dict["description"],
                area=g.area,
                type=dict["type"],
                management = dict["management"],
                equipment = dict["equipment"],
                geom=g)
        b.save()
        print(b.id)
    
    def update(self,dict):
        pass

    def select(self,dict):
        pass

    def delete(self,dict):
        pass