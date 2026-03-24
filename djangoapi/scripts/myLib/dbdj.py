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
            return d
        except Exception as e:
                d = {"ok": False,
                    "message": str(e),
                    "data": None}
                return d
    
    def selectallAsDicts(self,model):
        l=model.objects.all()
        data=[]
        for b in l:
            dict=model_to_dict(b)
            data.append(dict)
        d = {'ok':True, 'message': 'Data retrieved', 'data': data}
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
            return d
        except Exception as e:
            d = {"ok": False,
                "message": str(e),
                "data": None}
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

            elif g.geom_type in ['Point']:
                inside = self.point_in_polygon(snapped_wkb_geometry)
                if not inside:
                    d = {'ok': False, 
                        'message':'Error: The point is outside all polygon layers',
                        'data': None}
                    return d
                intersections = self.st_relate(table,snapped_wkb_geometry,'T********')
            if intersections:
                d = {'ok': False, 
                    'message':'The geometry interior intersects with the following geometries id',
                    'data': intersections}
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
            return d
        except Exception as e:
            d = {"ok": False,
                "message": str(e),
                "data": None}
            return d
    
    def update(self,model,dict,table):
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
                return d
            print('Valid Geometry')
            
            #Check intersections with another geometry in the same layer:
            if g.geom_type in ['Polygon','LineString']:
                intersections = self.st_relate(table,snapped_wkb_geometry,'T********',dict['id'], update=True)
                
            elif g.geom_type in ['Point']:
                inside = self.point_in_polygon(snapped_wkb_geometry)
                if not inside:
                    d = {'ok': False, 
                        'message':'Error: The point is outside all polygon layers',
                        'data': None}
                    return d
                intersections = self.st_relate(table,snapped_wkb_geometry,'T********',dict['id'], update=True)
            if intersections:
                    d = {'ok': False, 
                        'message':'The geometry interior intersects with the following geometries id',
                        'data': intersections}
                    return d
            #Recalc area, dist and data creation
            if g.geom_type == 'Polygon':
                dict['area']=g.area
            elif g.geom_type == 'LineString':
                dict['dist']=g.length
            dict['geom']=g 
            #Execute Update
            p = model.objects.filter(id=dict['id']).update(**dict)
            if p:
                d = {"ok": True,
                    "message": "Data updated",
                    "data": [{"rows_updated": 1}]}
            else:
                d = {"ok":False,
                    "message":"No row found with that id",
                    "data":None}
            return d
        except Exception as e:
                d = {"ok": False,
                    "message": str(e),
                    "data": None}
                return d

    #Geometry and Topology Tools
    def geomToSnappedWkb(self,geom):
        '''WKT to Snapped WKB'''
        query="select st_snaptogrid(st_geomfromtext(%s, %s),%s)"
        self.cur.execute(query, [geom,EPSG_CODE, SNAPTOGRIDDEC])
        snapped_wkb_geometry=self.cur.fetchall()[0][0]
        #print(f'snapped_wkb_geometry: {snapped_wkb_geometry}')
        return snapped_wkb_geometry
    
    def st_relate(self,table,geom,matrix,id=None,update=False):
        if update:
            query=f""" 
                    select id from {table} where ST_relate(
                        geom,
                        %s,
                        '{matrix}') and id != %s
                """
            self.cur.execute(query,[geom,id])
        else:
            query=f""" 
                    select id from {table} where ST_relate(
                        geom,
                        %s,
                        '{matrix}')
                    """
            self.cur.execute(query,[geom])
        relate = self.cur.fetchall()
        return relate
        
    def point_in_polygon(self,g):
        query="""
                    SELECT id
                    FROM infraverde_parks
                    WHERE ST_Within(%s,geom)
                ;
                """
        self.cur.execute(query,[g])
        return self.cur.fetchall()
        
        
         
