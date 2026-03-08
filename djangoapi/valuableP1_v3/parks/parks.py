from psycopg.rows import dict_row
#from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE,SNAPTOGRIDDEC
from myLib.database import Database as Db


class Parks(Db):
    def __init__(self):
        super().__init__()
        self.table = 'apm.parks'
        self.fields = 'id, description, area, type, management, equipment, st_astext(geom)'
        
    def insert(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],self.table)
        Db.insert(self,self.table,dict)

    def update(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],self.table,dict['id'],command='update')
        Db.update(self,self.table,dict)

    def select(self, dict, asDict=False):
        Db.select(self,self.table,self.fields,dict['id'],asDict)

    def delete(self,dict):
        Db.delete(self,table=self.table,id=dict['id'])

            
