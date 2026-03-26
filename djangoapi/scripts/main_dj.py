import sys

from scripts.p1_django.parks.parks_crud import Parks_crud
from scripts.p1_django.trees.trees_crud import Trees_crud
from scripts.p1_django.corridors.corridors_crud import Corridors_crud

#python manage.py runscript main_dj --script-args parks selectAsDict
#python manage.py runscript main_dj --script-args parks selectAsTuple
#python manage.py runscript main_dj --script-args parks insert
park_insert_dict = {
        'description':'My first park',
        'area':1500,
        'type':'Historic',
        'management':'Municipal',
        'equipment':True,
        'geom':'POLYGON ((728819.67173501581419259 4373398.11045156698673964, 728845.91893531451933086 4373477.20201513357460499, 729006.90176381275523454 4373421.20798782911151648, 728975.40512345440220088 4373323.5684027187526226, 728884.76479175640270114 4373363.46414717193692923, 728819.67173501581419259 4373398.11045156698673964))'}
        #'geom': 'POLYGON ((728855.98036209610290825 4373352.87777639459818602, 728877.67804767633788288 4373402.57247562613338232, 728916.17394144763238728 4373381.57471538707613945, 728898.67580791527871042 4373336.7794935442507267, 728855.98036209610290825 4373352.87777639459818602))'} #Interseca con el poligono anterior
park_select_dict = {'id':8}
park_update_dict = {
           'id':6,
           'description':'My first park updated',
           'area':3000,
           'type':'Historic',
           'management':'Municipal',
           'equipment':False,
           'geom':'POLYGON ((728819.67173501581419259 4373398.11045156698673964, 728845.91893531451933086 4373477.20201513357460499, 729006.90176381275523454 4373421.20798782911151648, 728975.40512345440220088 4373323.5684027187526226, 728884.76479175640270114 4373363.46414717193692923, 728819.67173501581419259 4373398.11045156698673964))'
}
park_delete_dict = {'id':6}

tree_insert_dict ={
           'description':'My first tree',
           'species':'Naranjo',
           'height':9.5,
           'condition':'Regular',
           'is_protected':False,
           'geom':'POINT (728945.48331511404830962 4373427.59480656683444977)' #Punto dentro de poligono
           #'geom':'POINT (729016.70071859075687826 4373409.5717290285974741)' #Punto fuera de poligono
}
tree_select_dict = {'id':22}
tree_update_dict ={
           'id':22,
           'description':'My first updated tree',
           'species':'Lemon',
           'height':17.2,
           'condition':'Good',
           'is_protected':True,
           'geom':'POINT (728945.48331511404830962 4373427.59480656683444977)'
}
tree_delete_dict = {'id':22}

corr_insert_dict ={
           'description':'Av.Naranjos',
           'dist':567.5,
           'type':'peatonal',
           'width':1,
           'lighting':True,
           'geom':'LINESTRING (729311.19430594204459339 4373088.30599737819284201, 728773.56415315857157111 4373270.46156745310872793)'
}
corr_select_dict = {'id':6}
corr_update_dict ={
           'description':'Av.Naranjos',
           'dist':567.5,
           'type':'ciclovia',
           'width':1.2,
           'lighting':True,
           'geom':'LINESTRING (729311.19430594204459339 4373088.30599737819284201, 728773.56415315857157111 4373270.46156745310872793)',
           'id':6
}
corr_delete_dict = {'id':6}

def run(*args):
    #print(args)
    #print(len(args))
    if len(args) == 2:
        tableName = args[0]
        functionName = args[1]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)

    if tableName not in ["parks", "trees", "corridors"]:
        print("Error: The available table names are parks, trees, corridors")
        sys.exit(0)
    
    if functionName not in ["insert", "selectAsTuple", "selectAsDict", "selectallAsDicts", "update", "delete"]:
        print("Error the available function names are insert, selectAsDict, selectAsTuple, selectallAsDicts, delete or update")
        sys.exit(0)

    if tableName == "parks":
        b=Parks_crud()
        if functionName=="insert":
            print(b.insert(park_insert_dict))
        elif functionName=="selectAsTuple":
            print(b.select(park_select_dict))
        elif functionName=="selectAsDict":
            print(b.select(park_select_dict,asDict=True))
        elif functionName=="selectallAsDicts":
            print(b.selectallAsDicts())
        elif functionName=="update":
            print(b.update(park_update_dict))
        elif functionName=="delete":
            print(b.delete(park_delete_dict))

    elif tableName=="trees":
        b=Trees_crud()
        if functionName=="insert":
            print(b.insert(tree_insert_dict))
        elif functionName=="selectAsTuple":
            print(b.select(tree_select_dict))
        elif functionName=="selectAsDict":
            print(b.select(tree_select_dict,asDict=True))
        elif functionName=="selectallAsDicts":
            print(b.selectallAsDicts())
        elif functionName=="update":
            print(b.update(tree_update_dict))
        elif functionName=="delete":
            print(b.delete(tree_delete_dict))

    elif tableName=="corridors":
        b=Corridors_crud()
        if functionName=="insert":
            print(b.insert(corr_insert_dict))
        elif functionName=="selectAsTuple":
            print(b.select(corr_select_dict))
        elif functionName=="selectAsDict":
            print(b.select(corr_select_dict, asDict=True))
        elif functionName=="selectallAsDicts":
            print(b.selectallAsDicts())
        elif functionName=="update":
            print(b.update(corr_update_dict))
        elif functionName=="delete":
            print(b.delete(corr_delete_dict))

if __name__ == "__main__":
    run()

