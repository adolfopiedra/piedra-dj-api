'''Tienes que crear dos funciones para modificar una tabla de base de datos: 
una usará SQL en bruto con psycopg y la otra usará modelos Django.

Para el examen tienes que saber:

Cómo definir los parámetros de una función y cómo devolver valores.
Cómo conectarse al examen de base de datos, user postgres psw postgres, host: postgis, puerto: 5432 (se me olvidó poner estos datos en el examen).
Cómo crear oraciones SQL básicas y usar los parámetros %s con psycopg.
Cómo usar modelos Django para gestionar datos de tablas.
Cómo usar comprobaciones de geometría para controlar los datos de entrada: st_relate, st_intersects, st_within, st_distance,'''

## Conexión a la base de datos usando psycopg
import psycopg

def connect():
    conn= psycopg.connect(
        dbname='exam',
        user='postgres',
        password='postgres',
        host='postgis',
        port=5432)
    print("Connected")
    return conn

def insert():
    conn=connect()
    cur=conn.cursor()
    cons="""
            INSERT INTO apm.parques(description, area, geom)
            VALUES (%s,%s,st_geometryFromText(%s,25830)) 
            RETURNING ID
        """
    cur.execute(cons,['park',20000,'POLYGON ((100 100, 200 100, 200 200, 100 200, 100 100))'])
    conn.commit()
    cur.close()
    conn.close()

    print("Inserted")

## Conexión a la base de datos usando django models