from psycopg.rows import dict_row
#from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE,SNAPTOGRIDDEC
from myLib.database import Database as Db


class Parks(Db):
    def __init__(self):
        super().__init__()
        
    def insert(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'])
        cons="""
        INSERT INTO apm.parks 
            (description, area, type, management, equipment, geom)
        VALUES
            (%s,%s,%s,%s,%s,
            st_snaptogrid(st_geometryFromText(%s,%s),%s))
        RETURNING id
        """
        try:
            self.cur.execute(cons,
                        [dict['description'], #descripcion
                        dict['area'], #area
                        dict['type'], #tipo
                        dict['management'], #gestion
                        dict['equipment'], #equipamiento
                        dict['geom'],
                        EPSG_CODE,
                        SNAPTOGRIDDEC
                        ])
            self.conn.commit()
            l=self.cur.fetchall()
            print('Inserted')
            print([{"id":l[0][0]}])
            self.disconnect()
            return {
            "ok": True,
            "message": "Data inserted",
            "data": [{"id":l[0][0]}]}
        except Exception as e:
            self.conn.rollback()
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
                }

    def select(self, dict, asDict=False):
        if asDict:
            #The rows are dicts
            self.cur=self.conn.cursor(row_factory=dict_row)
        
        cons="""
        SELECT 
            id, description, area, type, management, equipment, st_astext(geom)
        FROM 
            apm.parks 
        WHERE
            id=%s
        """
        try:
            self.cur.execute(cons, [dict['id']])
            l=self.cur.fetchall()
            self.disconnect()
            if len(l)>0:
                print(f"{len(l)} Selected")
                print(l)
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
            self.conn.rollback()
            self.disconnect()
            return {
                "ok": False,
                "message": str(e),
                "data": None
            }

    def update(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],dict['id'],command='update')
        cons="""
            UPDATE
                apm.parks 
            SET 
                (description, area, type, management, equipment, geom) = ROW(%s,%s,%s,%s,%s, st_snaptogrid(st_geometryFromText(%s,%s),%s))    
            WHERE
                id=%s
            """
        valuesList=[dict['description'], #descripcion
                    dict['area'], #area
                    dict['type'], #tipo
                    dict['management'], #gestion
                    dict['equipment'], #equipamiento
                    dict['geom'],
                    EPSG_CODE,
                    SNAPTOGRIDDEC,
                    dict['id']]
        
        try:
            self.cur.execute(cons, valuesList)
            affected_rows = self.cur.rowcount
            self.conn.commit()

            if affected_rows > 0:
                print([{f'rows_updated:{affected_rows}, id:{dict['id']}'}])
                self.disconnect()
                return {
                    "ok": True,
                    "message": "Data updated",
                    "data": [{f'rows_updated:{affected_rows}'}]
                }
            else:
                print('No row found with that id')
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

    def delete(self,dict):
        cons="""
            DELETE FROM
                apm.parks  
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        try:
            self.cur.execute(cons, [dict['id']])
            affected_rows = self.cur.rowcount
            self.conn.commit()
            
            if affected_rows > 0:
                print(f'id:{dict['id']} Deleted')
                self.disconnect()
                return {
                    "ok": True,
                    "message": "Data deleted",
                    "data": [{"rows_deleted": affected_rows}]
                }
            else:
                print('No row found with that id')
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

            
