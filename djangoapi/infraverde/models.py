from django.db import models
from django.contrib.gis.db import models as gis_models  # deactivate in windows. You don't have GEOS
import django.utils.timezone as djangoTimezone

from codelist.models import (
    ParkType,
    ParkManagement,
    CorridorType,
    TreeSpecies,
    TreeCondition
)


class Parks(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    area = models.FloatField(blank=True, null=True)

    type = models.ForeignKey(ParkType, on_delete=models.PROTECT, blank=True, null=True)
    management = models.ForeignKey(ParkManagement, on_delete=models.PROTECT, blank=True, null=True)

    equipment = models.BooleanField(blank=True, null=True)
    geom = gis_models.PolygonField(srid=25830, blank=True, null=True)
    data_creation = models.DateTimeField(blank=True, db_default=djangoTimezone.now())


class Trees(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    species = models.ForeignKey(TreeSpecies, on_delete=models.PROTECT, blank=True, null=True)

    height = models.FloatField(blank=True, null=True)

    condition = models.ForeignKey(TreeCondition, on_delete=models.PROTECT, blank=True, null=True)

    is_protected = models.BooleanField(blank=True, null=True)
    geom = gis_models.PointField(srid=25830, blank=True, null=True)
    data_creation = models.DateTimeField(blank=True, db_default=djangoTimezone.now())


class Corridors(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    dist = models.FloatField(blank=True, null=True)

    type = models.ForeignKey(CorridorType, on_delete=models.PROTECT, blank=True, null=True)

    width = models.FloatField(blank=True, null=True)
    lighting = models.BooleanField(blank=True, null=True)
    geom = gis_models.LineStringField(srid=25830, blank=True, null=True)
    data_creation = models.DateTimeField(blank=True, db_default=djangoTimezone.now())


# from django.db import models
# from django.contrib.gis.db import models as gis_models #deactivate in windows. You don have GEOS
# import django.utils.timezone as djangoTimezone
# # Create your models here.
# class Parks(models.Model):
#     id = models.AutoField(primary_key=True)
#     description = models.CharField(max_length=100,blank=True,null=True)
#     area = models.FloatField(blank=True,null=True)
#     type = models.CharField(max_length=100,blank=True,null=True)
#     management = models.CharField(max_length=100,blank=True,null=True)
#     equipment = models.BooleanField(blank=True,null=True)
#     geom = gis_models.PolygonField(srid=25830,blank=True,null=True)
#     data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

# class Trees(models.Model):
#     id = models.AutoField(primary_key=True)
#     description = models.CharField(max_length=100,blank=True,null=True)
#     species = models.CharField(max_length=100,blank=True,null=True)
#     height = models.FloatField(blank=True,null=True)
#     condition = models.CharField(max_length=100,blank=True,null=True)
#     is_protected = models.BooleanField(blank=True,null=True)
#     geom = gis_models.PointField(srid=25830,blank=True,null=True)
#     data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

# class Corridors(models.Model):
#     id = models.AutoField(primary_key=True)
#     description = models.CharField(max_length=100,blank=True,null=True)
#     dist = models.FloatField(blank=True,null=True)
#     type = models.CharField(max_length=100,blank=True,null=True)
#     width = models.FloatField(blank=True,null=True)
#     lighting = models.BooleanField(blank=True,null=True)
#     geom = gis_models.LineStringField(srid=25830,blank=True,null=True)
#     data_creation = models.DateTimeField(blank = True, db_default=djangoTimezone.now())

#python manage.py startapp nombre   
#Pasar tablas
#python manage.py makemigrations
#python manage.py migrate