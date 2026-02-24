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
            INSERT INTO apm.parques(description, area, geom)
            VALUES (%s,%s,st_geometryFromText(%s,25830)) 
            RETURNING ID
        """
    cur.execute(cons,['upv02',9654.489,'POLYGON ((728682.04891478247009218 4373483.63257919624447823, 728696.39738427905831486 4373525.62809967342764139, 728839.88207924494054168 4373479.08306447695940733, 728812.93495360505767167 4373402.09127693437039852, 728729.99380066129378974 4373451.08605082519352436, 728682.04891478247009218 4373483.63257919624447823))'])
    conn.commit()
    cur.close()
    conn.close()

    print("Inserted")

