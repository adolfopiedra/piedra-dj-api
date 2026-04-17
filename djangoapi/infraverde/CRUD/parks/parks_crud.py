#django Libraries
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.db import connection
from django.forms.models import model_to_dict

from scripts.myLib.dbdj import DbDjango as dbdj
from infraverde.models import Parks


class Parks_crud(dbdj):
    def __init__(self):
        super().__init__()

    def insert(self,dict):
        return dbdj.insert(self,Parks,dict,'infraverde_parks')
        
    def update(self,dict):
        return dbdj.update(self,Parks,dict,'infraverde_parks')

    def select(self,dict,asDict=False):
        return dbdj.select(self,Parks,dict,asDict)
    
    def selectallAsDicts(self):
        return dbdj.selectallAsDicts(self,Parks)
        
    def delete(self,dict):
        return dbdj.delete(self,Parks,dict)
