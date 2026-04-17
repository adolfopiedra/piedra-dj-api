from django.contrib.gis.geos import GEOSGeometry
from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Corridors
from django.http import JsonResponse

class Corridors_crud(dbdj):
    def __init__(self):
        super().__init__()

    def insert(self,dict):
        return dbdj.insert(self,Corridors,dict,'infraverde_corridors')

    def update(self,dict):
        return dbdj.update(self,Corridors,dict,'infraverde_corridors')
 
    def select(self,dict,asDict=False):
        return dbdj.select(self,Corridors,dict,asDict)
    
    def selectallAsDicts(self):
        return dbdj.selectallAsDicts(self,Corridors)
        
    def delete(self,dict):
        return dbdj.delete(self,Corridors,dict)
