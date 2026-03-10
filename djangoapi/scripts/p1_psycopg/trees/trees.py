from psycopg.rows import dict_row
from myLib.p1Settings import EPSG_CODE,SNAPTOGRIDDEC
from myLib.dbpg import DbPsycopg as Db


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
        return Db.insert(self,self.table,dict)
        
    def select(self, dict, asDict=False):
        return Db.select(self,self.table,self.fields,dict['id'],asDict)
        

    def update(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],self.table,id=dict['id'],command='update')
        for polygon_table in self.polygon_tables:
            Db.point_in_polygon(self,dict['geom'],polygon_table)
        return Db.update(self,self.table,dict)
        
    def delete(self,dict):
        return Db.delete(self,table=self.table,id=dict['id'])
