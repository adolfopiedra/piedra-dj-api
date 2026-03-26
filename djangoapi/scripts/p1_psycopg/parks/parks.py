from psycopg.rows import dict_row
from myLib.p1Settings import EPSG_CODE,SNAPTOGRIDDEC
from myLib.dbpg import DbPsycopg as Db


class Parks(Db):
    def __init__(self):
        super().__init__()
        self.table = 'apm.parks'
        self.fields = 'id, description, area, type, management, equipment, st_astext(geom) as geom'
        
    def insert(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],self.table)
        return Db.insert(self,self.table,dict)

    def update(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],self.table,dict['id'],command='update')
        return Db.update(self,self.table,dict)

    def select(self, dict, asDict=False):
        return Db.select(self,self.table,self.fields,dict['id'],asDict)

    def delete(self,dict):
        return Db.delete(self,table=self.table,id=dict['id'])

            
