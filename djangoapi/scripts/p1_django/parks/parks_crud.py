#django Libraries
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.db import connection
from django.forms.models import model_to_dict

from scripts.myLib.p1Settings import EPSG_CODE, SNAPTOGRIDDEC
from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Parks


class Parks_crud(dbdj):
    def __init__(self):
        super().__init__()

    def insert(self,dict):
        return dbdj.insert(self,Parks,dict,'infraverde_parks')
        # try:
        #     #Get the snapped wkb format for the geometry:
        #     snapped_wkb_geometry = dbdj.geomToSnappedWkb(self,dict['geom'])

        #     #Check if geometry is valid:
        #     g = GEOSGeometry(snapped_wkb_geometry, srid=EPSG_CODE)
        #     if not g.valid:
        #         d={'ok': False,
        #         'message': g.valid_reason,
        #         'data':None}
        #         print(d)
        #         return d
        #     print('Valid Geometry')

        #     #Now we can check if it intersects with another geomtry in the same layer
        #     #check if the geometry intersects any existing geometry
        #     query=""" 
        #             select id from infraverde_parks where ST_relate(
        #                 geom,
        #                 %s,
        #                 'T********')
        #         """
        #     self.cur.execute(query, [snapped_wkb_geometry])
        #     r=self.cur.fetchall()

        #     if len(r)>0:
        #         d = {'ok': False, 
        #             'message':'The geometry interior intersects with the following geometries id',
        #             'data': r}
        #         print(d)
        #         return d
            
        #     #Insert the data
        #     dict['geom']=g
        #     p = Parks(**dict)
        #     p.save()

        #     data=model_to_dict(p)
        #     data['geom']=g.wkt
        #     data['data_creation']=data['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

        #     d = {"ok": True,
        #         "message": "Data inserted",
        #         "data": [data]}
            
        #     print(d)
        #     return d
        # except Exception as e:
        #         d = {"ok": False,
        #             "message": str(e),
        #             "data": None}
        #         print(d)
        #         return d
        
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

            dict['geom']=g
            dict['area']=g.area
            p = Parks.objects.filter(id=dict['id']).update(**dict)
            if p > 0:
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
