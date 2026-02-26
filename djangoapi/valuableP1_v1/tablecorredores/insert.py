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
            INSERT INTO apm.corredores(description, dist, geom)
            VALUES (%s,%s,st_geometryFromText(%s,25830)) 
            RETURNING ID
        """
    cur.execute(cons,['Ciclovia',926.521,'LINESTRING (728773.91411582741420716 4373270.24284076597541571, 727896.20773784175980836 4373567.71111082006245852)'])
    conn.commit()
    cur.close()
    conn.close()

    print("Inserted")

