#https://urianviera.com/django/metodos-comunes-en-django

from django.forms.models import model_to_dict
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry

from scripts.myLib.p1Settings import EPSG_CODE, SNAPTOGRIDDEC


class DbDjango():
    def __init__(self):
        self.cur=connection.cursor()

    def select(self,model,dict,asDict):
        try:
            b = model.objects.filter(id=dict['id']).first() #id__gt = gmayor que
            if b:
                data = model_to_dict(b)
                data['geom']=b.geom.wkt
                data['data_creation']=data['data_creation'].strftime("%Y-%m-%d %H:%M:%S")
                if not asDict:
                    data = tuple(data.values())

                d = {"ok": True,
                    "message": "Data retrieved",
                    "data": [data]}
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
    
    def selectallAsDicts(self,model):
        l=model.objects.all()
        data=[]
        for b in l:
            dict=model_to_dict(b)
            data.append(dict)
        d = {'ok':True, 'message': 'Data retrieved', 'data': data}
        print(d)
        return d

    def delete(self,model,dict):
        try:
            b = model.objects.filter(id=dict['id']).first()
            if b:
                b.delete()
                d = {"ok": True,
                    "message": "Data deleted",
                    "data": [{"rows_deleted": 1}]}
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

    def insert(self,model,dict,table):
        try:
            #Get the snapped wkb format for the geometry:
            snapped_wkb_geometry = self.geomToSnappedWkb(dict['geom'])

            #Create GEOS Geometry Object
            g = GEOSGeometry(snapped_wkb_geometry, srid=EPSG_CODE)

            #Check if GEOS Geometry is valid:
            if not g.valid:
                d={'ok': False,
                'message': g.valid_reason,
                'data':None}
                print(d)
                return d
            print('Valid Geometry')

            #Check intersections with another geometry in the same layer:
            if g.geom_type in ['Polygon','LineString']:
                intersections = self.st_relate(table,snapped_wkb_geometry,'T********')
                if len(intersections) > 0:
                    d = {'ok': False, 
                        'message':'The geometry interior intersects with the following geometries id',
                        'data': intersections}
                    print(d)
                    return d
            elif g.geom_type in ['Point']:
                inside = self.point_in_polygon(snapped_wkb_geometry)
                if inside > 0:
                    d = {'ok': False, 
                        'message':'Error: The point is outside all polygon layers',
                        'data': None}
                    print(d)
                    return d

            
            
            #Insert the data
            if g.geom_type == 'Polygon':
                dict['area']=g.area
            elif g.geom_type == 'LineString':
                dict['dist']=g.length
            dict['geom']=g
            p = model(**dict)
            p.save()

            data=model_to_dict(p)
            data['geom']=g.wkt
            data['data_creation']=data['data_creation'].strftime("%Y-%m-%d %H:%M:%S")

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
    
    def update(self,model,dict,table):
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
            query=f""" 
                    select id from {table} where ST_relate(
                        geom,
                        %s,
                        'T********') and id != %s
                """
            cur.execute(query, [snapped_wkb_geometry, dict['id']])
            r=cur.fetchall()

            if len(r)>0:
                d = {'ok': False, 
                    'message':'The geometry interior intersects with the following geometries id',
                    'data': r}
                print(d)
                return d

            #Recalc area or dist
            if g.geom_type == 'Polygon':
                dict['area']=g.area
            elif g.geom_type == 'LineString':
                dict['dist']=g.length
            elif g.geom_type == 'Point':
                pass
            dict['geom']=g 

            p = model.objects.filter(id=dict['id']).first().update(**dict)

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





    #Geometry and Topology Tools
    def geomToSnappedWkb(self,geom):
        '''WKT to Snapped WKB'''
        query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
        self.cur.execute(query, [geom,EPSG_CODE, SNAPTOGRIDDEC])
        snapped_wkb_geometry=self.cur.fetchall()[0][0]
        #print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')
        return snapped_wkb_geometry
    
    def st_relate(self,table,geom,matrix):
        query=f""" 
                select id from {table} where ST_relate(
                    geom,
                    %s,
                    '{matrix}')
                """
        self.cur.execute(query,[geom])
        return self.cur.fetchall()
        
    def point_in_polygon(self,g):
        #snapped_wkb_geometry = self.geomToSnappedWkb(geom)
        #Create GEOS Geometry Object
        #g = GEOSGeometry(g, srid=EPSG_CODE)
        query="""
                    SELECT id
                    FROM infraverde_parks
                    WHERE ST_Within(%s,geom)
                ;
                """
        self.cur.execute(query,[g])
        return self.cur.fetchone()[0]
