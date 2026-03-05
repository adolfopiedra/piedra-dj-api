from django.db import models
from django.contrib.gis.db import models as gis_models #deactivate in windows. You don have GEOS
# Create your models here.

# Create your models here.
class Parks(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100,blank=True,null=True)
    area = models.FloatField(blank=True,null=True)
    perimeter = models.FloatField(blank=True,null=True)
    geom = gis_models.PolygonField(srid=25830,blank=True,null=True)
    height = models.FloatField(blank=True,null=True)
#python manage.py startapp nombre   
#Pasar tablas
#python manage.py makemigrations
#python manage.py migrate