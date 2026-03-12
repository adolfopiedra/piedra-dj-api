import sys

from scripts.p1_django.parks.parks_crud import Parks_crud
from scripts.p1_django.trees.trees_crud import Trees_crud
from scripts.p1_django.corridors.corridors_crud import Corridors_crud

#python manage.py runscript main_dj --script-args parks selectAsDict
#python manage.py runscript main_dj --script-args parks selectAsTuple
#python manage.py runscript main_dj --script-args parks insert


park_insert_dict ={
           'description':'My Second django park',
           'type':'Urban',
           'management':'Local',
           'equipment':True,
           'geom':'POLYGON ((728676.40576671902090311 4373547.23829459585249424, 728687.07962817384395748 4373578.25373628176748753, 728694.21011758828535676 4373575.97897892259061337, 728683.31752946437336504 4373544.78855590149760246, 728676.40576671902090311 4373547.23829459585249424))'
}
park_select_dict = {'id':3}
park_update_dict = {
           'id':3,
           'description':'My first park update django',
           'type':'Historic',
           'management':'Municipal',
           'equipment':False,
           'geom':'POLYGON ((728651.33969043404795229 4373712.07071246579289436, 728717.13267251593060791 4373691.07295222673565149, 728683.53625613369513303 4373597.98288183473050594, 728617.04334871040191501 4373618.28071673214435577, 728651.33969043404795229 4373712.07071246579289436))'
}
park_delete_dict = {'id':2}

tree_insert_dict ={
           'description':'My first dict tree',
           'species':'Naranjo',
           'height':9.5,
           'condition':'Regular',
           'is_protected':False,
           'geom':'POINT (728688.3482428549323231 4373571.5169548699632287)'
}
tree_select_dict = {'id':1}
tree_update_dict ={
           'id':13,
           'description':'My first update with db class',
           'species':'Lemon',
           'height':17.2,
           'condition':'Good',
           'is_protected':True,
           'geom':'POINT (728683.44876546587329358 4373557.60593871213495731)'
}
tree_delete_dict = {'id':2}

corr_insert_dict ={
           'description':'Av.Naranjos',
           'type':'peatonal',
           'width':1,
           'lighting':True,
           'geom':'LINESTRING (728913.98667475546244532 4373514.86674755252897739, 728893.68883985781576484 4373522.74090764205902815, 728891.41408249863889068 4373519.06629960052669048, 728860.09242347558028996 4373529.91514238994568586)'
}
corr_select_dict = {'id':2}
corr_update_dict ={
           'description':'Puente',
           'type':'pedestrian',
           'width':1,
           'lighting':True,
           'geom':'LINESTRING (728773.91411582741420716 4373270.24284076597541571, 727896.20773784175980836 4373567.71111082006245852)',
           'id':4
}
corr_delete_dict = {'id':4}

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
            b.insert(park_insert_dict)
        elif functionName=="selectAsTuple":
            b.select(park_select_dict)
        elif functionName=="selectAsDict":
            b.select(park_select_dict,asDict=True)
        elif functionName=="selectallAsDicts":
            b.selectallAsDicts()
        elif functionName=="update":
            b.update(park_update_dict)
        elif functionName=="delete":
            b.delete(park_delete_dict)

    elif tableName=="trees":
        b=Trees_crud()
        if functionName=="insert":
            b.insert(tree_insert_dict)
        elif functionName=="selectAsTuple":
            b.select(tree_select_dict)
        elif functionName=="selectAsDict":
            b.select(tree_select_dict,asDict=True)
        elif functionName=="selectallAsDicts":
            b.selectallAsDicts()
        elif functionName=="update":
            b.update(tree_update_dict)
        elif functionName=="delete":
            b.delete(tree_delete_dict)

    elif tableName=="corridors":
        b=Corridors_crud()
        if functionName=="insert":
            b.insert(corr_insert_dict)
        elif functionName=="selectAsTuple":
            b.select(corr_select_dict)
        elif functionName=="selectAsDict":
            b.select(corr_select_dict, asDict=True)
        elif functionName=="selectallAsDicts":
            b.selectallAsDicts()
        elif functionName=="update":
            b.update(corr_update_dict)
        elif functionName=="delete":
            b.delete(corr_delete_dict)

if __name__ == "__main__":
    run()

