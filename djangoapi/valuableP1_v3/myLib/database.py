from myLib import p1Settings
from myLib.p1Settings import EPSG_CODE
from myLib.p1Settings import SNAPTOGRIDDEC
import sys
import psycopg
from psycopg import sql

class Database():
    def __init__(self):
        self.conn=self.connect()
        self.cur=self.conn.cursor()

   
    #User Methods
    def connect(self):
        conn= psycopg.connect(
            dbname=p1Settings.POSTGRES_DB,
            user=p1Settings.POSTGRES_USER,
            password=p1Settings.POSTGRES_PASSWORD,
            host=p1Settings.POSTGRES_HOST,
            port=p1Settings.POSTGRES_PORT
            )
        print("Connected")
        return conn
    
    def disconnect(self):
        self.cur.close()
        self.conn.close()
        print('Disconnected')

    def is_valid(self,geom):
        #check if the geometry is valid after having simplified it
        cons ="""
                select ST_isvalid(
                st_snaptogrid(
                st_geomfromtext(%s, %s),
                %s
                )
                ) as is_valid
                """
        try:
            self.cur.execute(cons,
                        [geom,
                        p1Settings.EPSG_CODE,
                        p1Settings.SNAPTOGRIDDEC
                        ])
            l=self.cur.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            self.disconnect()
            sys.exit()
        if l[0][0]:
            print("The geometry is valid")
        else:
            print("Error: The geometry is not valid")
            self.disconnect()
            sys.exit()
    
    def check_intersection(self,geom,id=0,command='insert'):
        cons = """SELECT GeometryType(ST_GeomFromText(%s,%s))"""
        self.cur.execute(cons,[geom, p1Settings.EPSG_CODE])
        gtype = self.cur.fetchone()[0]

        if gtype == 'POLYGON':
            #check if the geometry intersects any existing geometry
            if command  == 'update':
                cons ="""
                    select id from apm.parks where ST_relate(
                    geom,
                    st_snaptogrid(
                    st_geomfromtext(%s, %s),
                    %s
                    ),'T********'
                    ) and id != %s
                    """
                valuelist = [geom,
                            p1Settings.EPSG_CODE,
                            p1Settings.SNAPTOGRIDDEC,
                            id]
            else: 
                cons ="""
                    select id from apm.parks where ST_relate(
                    geom,
                    st_snaptogrid(
                    st_geomfromtext(%s, %s),
                    %s
                    ),'T********'
                    )
                    """
                valuelist = [geom,
                            p1Settings.EPSG_CODE,
                            p1Settings.SNAPTOGRIDDEC]
            try:
                self.cur.execute(cons,valuelist)
                l=self.cur.fetchall()
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                sys.exit()
            if len(l)>0:
                print("Error: There are geometrys that intersect with the new geometry")
                self.disconnect()
                sys.exit()
            else:
                print("The new geometry does not intersect any existing geometry")
        
        elif gtype == 'LINESTRING':
            if command  == 'update':
                cons = """
                        SELECT id
                        FROM apm.corridors
                        WHERE ST_Intersects(
                            geom,
                            st_snaptogrid(
                                st_geomfromtext(%s,%s),
                                %s
                            )
                        ) and id != %s
                        """
                valuelist = [geom,
                            p1Settings.EPSG_CODE,
                            p1Settings.SNAPTOGRIDDEC,
                            id]
            else:
                cons = """
                        SELECT id
                        FROM apm.corridors
                        WHERE ST_Intersects(
                            geom,
                            st_snaptogrid(
                                st_geomfromtext(%s,%s),
                                %s
                            )
                        )
                        """
                valuelist = [geom,
                            p1Settings.EPSG_CODE,
                            p1Settings.SNAPTOGRIDDEC]
            try:
                self.cur.execute(cons,valuelist)
                l=self.cur.fetchall()
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                sys.exit()
            if len(l)>0:
                print("Error: There are geometrys that intersect with the new geometry")
                self.disconnect()
                sys.exit()
            else:
                print("The new geometry does not intersect any existing geometry")
            
        elif gtype == 'POINT':
            cons = """
                SELECT id AS table_name
                FROM apm.parks
                WHERE ST_Within(ST_SnapToGrid(ST_GeomFromText(%s,%s), %s), geom)
                UNION ALL
                SELECT id
                FROM apm.corridors
                WHERE ST_Within(ST_SnapToGrid(ST_GeomFromText(%s,%s), %s), geom)
                UNION ALL
                SELECT id
                FROM apm.trees
                WHERE ST_Within(ST_SnapToGrid(ST_GeomFromText(%s,%s), %s), geom)
            """
            valuelist = [
                geom, EPSG_CODE, SNAPTOGRIDDEC,
                geom, EPSG_CODE, SNAPTOGRIDDEC,
                geom, EPSG_CODE, SNAPTOGRIDDEC
            ]

            try:
                self.cur.execute(cons, valuelist)
                l = self.cur.fetchall()
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                sys.exit()

            if l:
                print("Error: Point falls inside an existing polygon in one of the layers")
                self.disconnect()
                sys.exit()
            else:
                print("The point is outside all polygon layers")
                