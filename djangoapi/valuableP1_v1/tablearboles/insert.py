import psycopg
from myLibs import p1Settings
def connect():
    conn = psycopg.connect(
        dbname=p1Settings.POSTGRES_DB,
        user=p1Settings.POSTGRES_USER,
        password=p1Settings.POSTGRES_PASSWORD,
        host=p1Settings.POSTGRES_HOST,
        port=p1Settings.POSTGRES_PORT
                        )
    print("Connected")
    return conn
    #conn.close()

def insert():
    conn=connect()
    cur=conn.cursor()
    cons="""
            INSERT INTO apm.arboles(description, especie, geom)
            VALUES (%s,%s,st_geometryFromText(%s,25830)) 
            RETURNING ID
        """
    cur.execute(cons,['Av. Naranjos','Naranjo','POINT (728926.0603868915932253 4373197.45060526859015226)'])
    conn.commit()
    cur.close()
    conn.close()

    print("Inserted")

