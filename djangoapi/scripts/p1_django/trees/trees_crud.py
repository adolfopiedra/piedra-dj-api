from django.contrib.gis.geos import GEOSGeometry
from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Trees
from django.http import JsonResponse


class Trees_crud(dbdj):
    def __init__(self):
        super().__init__()
    def insert(self,dict):
        return dbdj.insert(self,Trees,dict,'infraverde_trees')
 
    def update(self,dict):
        return dbdj.update(self,Trees,dict,'infraverde_trees')

    def select(self,dict,asDict=False):
        return dbdj.select(self,Trees,dict,asDict)
    
    def selectallAsDicts(self):
        return dbdj.selectallAsDicts(self,Trees)
        
    def delete(self,dict):
        return dbdj.delete(self,Trees,dict)
