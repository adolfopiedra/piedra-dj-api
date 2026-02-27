import sys
from parques.parquesOOP import ParquesOOP
from arboles.arbolesOOP import ArbolesOOP
from corredores.corredoresOOP import CorredoresOOP

def main():
    # sys.argv[0] es siempre el nombre del archivo (main.py)
    # Por eso verificamos que haya al menos 3 elementos (nombre + p1 + p2)
    if len(sys.argv) == 3:
        tableName = sys.argv[1]
        functionName = sys.argv[2]     
    else:
        print("Error: You mus give two parameters tableName and functionName to execute the addecuate function.")
        sys.exit(0)

    if tableName not in ["parques", "arboles", "corredores"]:
        print("Error: The available table names are parques, arboles, corredores")
        sys.exit(0)
    
    if functionName not in ["insert", "select", "selectAsDict", "update", "delete"]:
        print("Error the available function names are insert, select, delete or update")
        sys.exit(0)

    if tableName == "parques":
        b=ParquesOOP()
        if functionName=="insert":
            b.insert()
        elif functionName=="select":
            b.select()
        elif functionName=="selectAsDict":
            b.select(asDict=True)
        elif functionName=="update":
            b.update()
        elif functionName=="delete":
            b.delete()

    elif tableName=="arboles":
        b=ArbolesOOP()
        if functionName=="insert":
            b.insert()
        elif functionName=="select":
            b.select()
        elif functionName=="update":
            b.update()
        elif functionName=="delete":
            b.delete()

    elif tableName=="corredores":
        b=CorredoresOOP()
        if functionName=="insert":
            b.insert()
        elif functionName=="select":
            b.select()
        elif functionName=="update":
            b.update()
        elif functionName=="delete":
            b.delete()

if __name__ == "__main__":
    main()

