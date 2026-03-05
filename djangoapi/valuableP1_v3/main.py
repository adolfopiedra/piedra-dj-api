import sys
from parks.parks import Parks
from trees.trees import Trees
from corridors.corridors import Corridors

park_insert_dict ={
           'description':'My first dict park',
           'area':1250,
           'type':'Historic',
           'management':'Municipal',
           'equipment':True,
           'geom':'POLYGON ((728682.04 4373483.63, 728696.39 4373525.62, 728839.88 4373479.08, 728812.93 4373402.09, 728729.99 4373451.08, 728682.04 4373483.63))'
}
park_select_dict = {'id':10}
park_update_dict = {
           'id':25,
           'description':'My first dict park update',
           'area':1250,
           'type':'Urban',
           'management':'Municipal',
           'equipment':False,
           'geom':'POLYGON ((728682.04 4373483.63, 728696.39 4373525.62, 728839.88 4373479.08, 728812.93 4373402.09, 728729.99 4373451.08, 728682.04 4373483.63))'
}
park_delete_dict = {'id':20}

tree_insert_dict ={
           'description':'My first dict tree',
           'species':'Naranjo',
           'height':9.5,
           'condition':'Regular',
           'is_protected':False,
           'geom':'POINT (728926.0603868915932253 4373197.45060526859015226)'
}
tree_select_dict = {'id':11}
tree_update_dict ={
           'id':6,
           'description':'My first update dict tree',
           'species':'Lemon',
           'height':17.2,
           'condition':'Good',
           'is_protected':True,
           'geom':'POINT (728926.0603868915932253 4373197.45060526859015226)'
}
tree_delete_dict = {'id':8}

corr_insert_dict ={
           'description':'Av.Naranjos',
           'dist':20,
           'type':'peatonal',
           'width':1,
           'lighting':True,
           'geom':'LINESTRING (728773.91411582741420716 4373270.24284076597541571, 727896.20773784175980836 4373567.71111082006245852)'
}
corr_select_dict = {'id':5}
corr_update_dict ={
           'description':'Puente',
           'dist':17.25,
           'type':'peatonal',
           'width':1,
           'lighting':True,
           'geom':'LINESTRING (728773.91411582741420716 4373270.24284076597541571, 727896.20773784175980836 4373567.71111082006245852)',
           'id':2
}
corr_delete_dict = {'id':4}

def main():
    # sys.argv[0] es siempre el nombre del archivo (main.py)
    # Por eso verificamos que haya al menos 3 elementos (nombre + p1 + p2)
    if len(sys.argv) == 3:
        tableName = sys.argv[1]
        functionName = sys.argv[2]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)

    if tableName not in ["parks", "trees", "corridors"]:
        print("Error: The available table names are parks, trees, corridors")
        sys.exit(0)
    
    if functionName not in ["insert", "selectAsTuple", "selectAsDict", "update", "delete"]:
        print("Error the available function names are insert, selectAsDict, selectAsTuple, delete or update")
        sys.exit(0)

    if tableName == "parks":
        b=Parks()
        if functionName=="insert":
            b.insert(park_insert_dict)
        elif functionName=="selectAsTuple":
            b.select(park_select_dict)
        elif functionName=="selectAsDict":
            b.select(park_select_dict,asDict=True)
        elif functionName=="update":
            b.update(park_update_dict)
        elif functionName=="delete":
            b.delete(park_delete_dict)

    elif tableName=="trees":
        b=Trees()
        if functionName=="insert":
            b.insert(tree_insert_dict)
        elif functionName=="selectAsTuple":
            b.select(tree_select_dict)
        elif functionName=="selectAsDict":
            b.select(tree_select_dict,asDict=True)
        elif functionName=="update":
            b.update(tree_update_dict)
        elif functionName=="delete":
            b.delete(tree_delete_dict)

    elif tableName=="corridors":
        b=Corridors()
        if functionName=="insert":
            b.insert(corr_insert_dict)
        elif functionName=="selectAsTuple":
            b.select(corr_select_dict)
        elif functionName=="selectAsDict":
            b.select(corr_select_dict, asDict=True)
        elif functionName=="update":
            b.update(corr_update_dict)
        elif functionName=="delete":
            b.delete(corr_delete_dict)

if __name__ == "__main__":
    main()

