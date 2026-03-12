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
           'geom':'POLYGON ((728610.8752566403709352 4373481.97025651764124632, 728645.17159836390055716 4373470.94643239211291075, 728633.97279290307778865 4373438.22492268681526184, 728600.5513578561367467 4373449.42372814752161503, 728610.8752566403709352 4373481.97025651764124632))'
}
park_select_dict = {'id':29}
park_update_dict = {
           'id':27,
           'description':'My first park update django',
           'area':3000,
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
           'geom':'POINT (728621.72409943037200719 4373459.57264559622853994)'
}
tree_select_dict = {'id':1}
tree_update_dict ={
           'id':1,
           'description':'My first update with db class',
           'species':'Lemon',
           'height':17.2,
           'condition':'Good',
           'is_protected':True,
           'geom':'POINT (728722.73207524628378451 4373551.08788396790623665)'
}
tree_delete_dict = {'id':2}

corr_insert_dict ={
           'description':'Av.Naranjos',
           'type':'peatonal',
           'width':1,
           'lighting':True,
           'geom':'LINESTRING (728913.98667475546244532 4373514.86674755252897739, 728893.68883985781576484 4373522.74090764205902815, 728891.41408249863889068 4373519.06629960052669048, 728860.09242347558028996 4373529.91514238994568586)'
}
corr_select_dict = {'id':1}
corr_update_dict ={
           'description':'Puente',
           'dist':17.25,
           'type':'pedestrian',
           'width':1,
           'lighting':True,
           'geom':'LINESTRING (728773.91411582741420716 4373270.24284076597541571, 727896.20773784175980836 4373567.71111082006245852)',
           'id':1
}
corr_delete_dict = {'id':2}

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

