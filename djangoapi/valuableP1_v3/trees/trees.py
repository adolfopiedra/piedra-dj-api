from psycopg.rows import dict_row
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE,SNAPTOGRIDDEC
from myLib.database import Database as Db


class Trees(Db):
    def __init__(self):
        super().__init__()
        self.table = 'apm.trees'
        self.fields = 'id,description,species,height,condition,is_protected,st_astext(geom)'
        self.polygon_tables = Db.get_tables_by_geom(self,'POLYGON')
    def insert(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],self.table)
        for polygon_table in self.polygon_tables:
            Db.point_in_polygon(self,dict['geom'],polygon_table)
        Db.insert(self,self.table,dict)
        
    def select(self, dict, asDict=False):
        Db.select(self,self.table,self.fields,dict['id'],asDict)
        

    def update(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],self.table,id=dict['id'],command='update')
        for polygon_table in self.polygon_tables:
            Db.point_in_polygon(self,dict['geom'],polygon_table)
        Db.update(self,self.table,dict)
        
    def delete(self,dict):
        Db.delete(self,table=self.table,id=dict['id'])
