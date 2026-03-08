from psycopg.rows import dict_row
from myLib import p1Settings
from myLib.p1Settings import EPSG_CODE,POSTGRES_SQUEMA,SNAPTOGRIDDEC
import sys
import psycopg
from psycopg import sql

class Database():
    def __init__(self):
        self.conn=self.connect()
        self.cur=self.conn.cursor()

    #User Methods
    #Conections to the database
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

    #General Methods
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
            print(f'Inserted. id:{new_id}')
            self.disconnect()

            return {
                "ok": True,
                "message": "Data inserted",
                "data": [{"id": new_id}]
            }

        except Exception as e:
            print(f'Error:{e}')
            self.conn.rollback()
            self.disconnect()

            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def update(self,table,dict):
        cols = [k for k in dict.keys() if k not in ['geom','id']]
        val_string = ",".join([f"{c}=%s" for c in cols]) + ",geom=ST_SnapToGrid(ST_GeomFromText(%s,%s),%s)"
        cons = f"""
            UPDATE {table}
            SET
            {val_string}
            WHERE id=%s
        """
        values = [dict[c] for c in cols] + [dict['geom'], EPSG_CODE, SNAPTOGRIDDEC, dict['id']]
        try:
            self.cur.execute(cons, values)
            self.conn.commit()
            affected_rows = self.cur.rowcount
        
            if affected_rows > 0:
                print(f'rows_updated:{affected_rows}')
                self.disconnect()
                return {
                    "ok": True,
                    "message": "Data updated",
                    "data": [{"rows_updated": affected_rows}]
                }
            else:
                self.disconnect()
                return {
                    "ok": False,
                    "message": "No row found with that id",
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
                self.disconnect()
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

    #Check Topology Methods
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
    
    def check_intersection(self,geom,table,id=None,command='insert'):
        cons = """SELECT GeometryType(ST_GeomFromText(%s,%s))"""
        self.cur.execute(cons,[geom, EPSG_CODE])
        gtype = self.cur.fetchone()[0]

        if gtype == 'POLYGON':
            #check if the geometry intersects any existing geometry
            if command  == 'update':
                cons =f"""
                    select id from {table} where ST_relate(
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
                cons =f"""
                    select id from {table} where ST_relate(
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
                cons = f"""
                        SELECT id
                        FROM {table}
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
                cons = f"""
                        SELECT id
                        FROM {table}
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
                cons = f"""
                        SELECT
                            EXISTS (
                                SELECT 1
                                FROM {table}
                                WHERE ST_Equals(geom, st_snaptogrid(ST_GeomFromText(%s,%s),%s))
                                and id != %s
                            );
                        """
                valuelist = [geom,
                             EPSG_CODE,
                             SNAPTOGRIDDEC,
                             id]
            else:
                cons = f"""
                        SELECT
                            EXISTS (
                                SELECT 1
                                FROM {table}
                                WHERE ST_Equals(geom, st_snaptogrid(ST_GeomFromText(%s,%s),%s))
                            );
                        """
                valuelist = [geom,EPSG_CODE,SNAPTOGRIDDEC]
            try:
                self.cur.execute(cons,valuelist)
                exists = self.cur.fetchone()[0]
            except Exception as e:
                print(f"Error: {e}")
                self.disconnect()
                sys.exit()

            if exists and command!='update':
                print("Error: The point with that geometry already exists")
                self.disconnect()
                sys.exit()
            else:
                print("The new geometry does not intersect any existing geometry")

    def point_in_polygon(self,geom,polygon_table):
        cons = f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM {POSTGRES_SQUEMA+'.'+polygon_table}
                    WHERE ST_Within(st_snaptogrid(ST_GeomFromText(%s,%s),%s),geom)
                );
                """
        try:
            self.cur.execute(cons,[geom,EPSG_CODE,SNAPTOGRIDDEC])
            inside = self.cur.fetchone()[0]
        except Exception as e:
            print(f"Error: {e}")
            self.disconnect()
            sys.exit()

        if not inside:
            print("Error: The point is outside all polygon layers")
            self.disconnect()
            sys.exit()

        print("The point falls inside a polygon layer")

    #Information Methods
    def get_tables_by_geom(self, geom_type):
        cons = f"""
                SELECT f_table_name
                FROM geometry_columns
                WHERE f_table_schema = '{POSTGRES_SQUEMA}'
                AND type = %s
                """
        try:
            self.cur.execute(cons, [geom_type])
            tables = [r[0] for r in self.cur.fetchall()]
            return tables
        except Exception as e:
            print(f"Error: {e}")
            self.disconnect()
            sys.exit()