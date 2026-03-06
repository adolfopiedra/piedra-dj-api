from psycopg.rows import dict_row
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

    def insert(self,table,dict):
        cols = [k for k in dict.keys() if k != 'geom']
        col_string = ",".join(cols) + ",geom"
        val_string = ",".join(["%s"] * len(cols)) + ", ST_SnapToGrid(ST_GeomFromText(%s,%s),%s)"

        cons = f"""
            INSERT INTO {table}
            ({col_string})
            VALUES
            ({val_string})
            RETURNING id
        """

        values = [dict[c] for c in cols] + [dict['geom'], EPSG_CODE, SNAPTOGRIDDEC]

        try:
            self.cur.execute(cons, values)
            self.conn.commit()
            new_id = self.cur.fetchall()[0][0]
            print(f'Inserted, id:{new_id}')
            self.disconnect()

            return {
                "ok": True,
                "message": "Data inserted",
                "data": [{"id": new_id}]
            }

        except Exception as e:
            self.conn.rollback()
            self.disconnect()

            return {
                "ok": False,
                "message": str(e),
                "data": None
            }


    def select(self,table,fields,id,asDict):
        if asDict:
            #The rows are dicts
            self.cur=self.conn.cursor(row_factory=dict_row)
        cons=f"""
        SELECT 
            {fields}
        FROM 
            {table} 
        WHERE
            id=%s
        """
        try:
            self.cur.execute(cons, [id])
            l=self.cur.fetchall()
            if len(l)>0:
                print(f"{len(l)} Selected")
                print(l)
                self.disconnect()
                return {
                    "ok": True,
                    "message": "Data retrieved",
                    "data": l
                }
            else:
                print(f"{len(l)} Selected")
                return {
                    "ok": False,
                    "message": "No data found",
                    "data": None
                }
        except Exception as e:
            print(f'Error: {e}')
            self.conn.rollback()
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def delete(self,table,id):
        cons=f"""
            DELETE FROM
                {table}  
            WHERE
                id=%s
            """
        try:
            self.cur.execute(cons, [id])
            affected_rows = self.cur.rowcount
            self.conn.commit()
            
            if affected_rows > 0:
                print(f"rows_deleted:{affected_rows}")
                self.disconnect()
                return {
                    "ok": True,
                    "message": "Data deleted",
                    "data": [{"rows_deleted": affected_rows}]
                }
            else:
                print(f"No row found with that id")
                return {
                    "ok": False,
                    "message": "No row found with that id",
                    "data": None
                }
        except Exception as e:
            self.conn.rollback()
            self.disconnect()

            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

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
    
    def check_intersection(self,geom,id=None,command='insert'):
        cons = """SELECT GeometryType(ST_GeomFromText(%s,%s))"""
        self.cur.execute(cons,[geom, EPSG_CODE])
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
            if command  == 'update':
                cons = """
                        SELECT
                            EXISTS (
                                SELECT 1
                                FROM apm.parks
                                WHERE ST_Within(st_snaptogrid(ST_GeomFromText(%s,%s),%s),geom)
                            ),
                            EXISTS (
                                SELECT 1
                                FROM apm.trees
                                WHERE ST_Equals(geom, st_snaptogrid(ST_GeomFromText(%s,%s),%s))
                                and id != %s
                            );
                        """
                valuelist = [geom,EPSG_CODE,SNAPTOGRIDDEC,geom,EPSG_CODE,SNAPTOGRIDDEC,id]
            else:
                cons = """
                        SELECT
                            EXISTS (
                                SELECT 1
                                FROM apm.parks
                                WHERE ST_Within(st_snaptogrid(ST_GeomFromText(%s,%s),%s),geom)
                            ),
                            EXISTS (
                                SELECT 1
                                FROM apm.trees
                                WHERE ST_Equals(geom, st_snaptogrid(ST_GeomFromText(%s,%s),%s))
                            );
                        """
                valuelist = [geom,EPSG_CODE,SNAPTOGRIDDEC,geom,EPSG_CODE,SNAPTOGRIDDEC]
            try:
                self.cur.execute(cons,valuelist)
                inside, exists = self.cur.fetchone()
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                sys.exit()
            if not inside:
                print("Error: The point is outside all polygon layers")
                self.disconnect()
                sys.exit()
            if exists and command!='update':
                print("Error: The point with that geometry already exists")
                self.disconnect()
                sys.exit()
            else:
                print("The new point falls inside an existing polygon in one of the layers")
                