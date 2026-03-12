#django Libraries
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.db import connection
from django.forms.models import model_to_dict

from scripts.myLib.p1Settings import EPSG_CODE, SNAPTOGRIDDEC
from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Parks

from datetime import datetime

class Parks_crud:
    def insert(self,dict):
        #return dbdj.insert(self,Parks,dict,'infraverde_parks')
        try:
            #we first get the snapped wkb format for the geometry:
            cur=connection.cursor()
            query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
            cur.execute(query, [dict['geom'],EPSG_CODE, SNAPTOGRIDDEC])
            snapped_wkb_geometry=cur.fetchall()[0][0]
            print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')

            #now we can check if it is valid as before:
            g = GEOSGeometry(snapped_wkb_geometry, srid=EPSG_CODE)
            if not g.valid:
                d={'ok': False,
                'message': g.valid_reason,
                'data':None}
                print(d)
                return d
            print('Valid Geometry')

            #Now we can check if it intersects with another geomtry in the same layer
            #check if the geometry intersects any existing geometry
            query=""" 
                    select id from infraverde_parks where ST_relate(
                        geom,
                        %s,
                        'T********')
                """
            cur.execute(query, [snapped_wkb_geometry])
            r=cur.fetchall()

            if len(r)>0:
                d = {'ok': False, 
                    'message':'The geometry interior intersects with the following geometries id',
                    'data': r}
                print(d)
                return d
            
            #Insert the data
            dict['geom']=g
            p = Parks(**dict)
            p.save()

            data=model_to_dict(p)
            data['geom']=g.wkt
            #data['data_creation']=data['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

            d = {"ok": True,
                "message": "Data inserted",
                "data": [data]}
            
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

            dict['geom']=g
            dict['area']=g.area
            p = Parks.objects.filter(id=dict['id']).update(**dict)
            if p > 0:
            #     p.area = g.area
            #     p.description = dict['description']
            #     p.type = dict['type']
            #     p.management = dict['management']
            #     p.equipment = dict['equipment']
            #     p.geom = g
            #     p.save()
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
