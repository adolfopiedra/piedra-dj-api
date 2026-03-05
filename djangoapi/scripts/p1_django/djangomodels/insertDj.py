from django.contrib.gis.geos import GEOSGeometry
from infraverde.models import Parks
from valuableP1_v3.myLib import p1Settings
# deactivate in windows. You don have GEOS
#create the geometry with geos
def run():
    g=GEOSGeometry('POLYGON((0 0, 10 0, 10 10, 0 11, 0 0))', srid=p1Settings.EPSG_CODE)
    if g.valid:
        print('Geometria Valida')
    #print the representation of the object
    print(g)
    #create a building object, from the model Buildings
    #b=Buildings(description='Edificio 1', area=100, geom=g)
    b=Parks(description='Park 01 con Django', area=g.area, perimeter=g.length,geom=g,height=100 )
    #saves it into the database
    b.save()
    #prints the asigned id of the object in the database
    print(b.id)
    #another way to create the object with a dictionary
    #d_of_values= {'description':'Edificio 1', 'area':2000}
    #you need to use the ** to unpack the dictionary
    #b=Parks(d_of_values)
    #b.save()
    #print(b.id)

    #python manage.py runscript 001_hello_script --script-args p1 p2 p3
    #python manage.py runscript scripts.p1_django.djangomodels.insertDj