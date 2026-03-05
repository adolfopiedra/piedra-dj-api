from psycopg.rows import dict_row
from pprint import pprint
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class Corridors():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self,dict):
        cons="""
        INSERT INTO apm.corridors 
            (description,dist,type,width,lighting,geom)
        VALUES
            (%s,%s,%s,%s,%s,
            st_geometryFromText(%s,%s))
        RETURNING id
        """
        try:
            self.cur.execute(cons,
                        [dict['description'],
                        dict['dist'],
                        dict['type'],
                        dict['width'],
                        dict['lighting'],
                        dict['geom'],
                        EPSG_CODE
                        ])
            
            self.conn.commit()
            l=self.cur.fetchall()
            self.disconnect()
            #print(cur.fetchall()[0][0]) <-- ERROR. YOU ONLY CAN FECTH THE RESULTS ONCE
            #print(l)
            #print(l[0][0])
            print('Inserted')
            print([{"id":l[0][0]}])
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
            id,description,dist,type,width,lighting,st_astext(geom)
        FROM 
            apm.corridors 
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

    def update(self, dict):
        cons="""
            UPDATE
                apm.corridors 
            SET 
                (description,dist,type,width,lighting,geom) = ROW(%s,%s,%s,%s,%s, st_geometryFromText(%s,%s))    
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=[dict['description'],
                        dict['dist'],
                        dict['type'],
                        dict['width'],
                        dict['lighting'],
                        dict['geom'],
                        EPSG_CODE,
                        dict['id']
                        ]
        try:
            self.cur.execute(cons, valuesList)
            affected_rows = self.cur.rowcount
            self.conn.commit()
            self.disconnect()

            if affected_rows > 0:
                print([{f'rows_updated:{affected_rows}'}])
                return {
                    "ok": True,
                    "message": "Data updated",
                    "data": [{f'rows_updated:{affected_rows}'}]
                }
            else:
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

    def delete(self,dict):
        cons="""
            DELETE FROM
                apm.corridors  
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
            self.disconnect()
            if affected_rows > 0:
                return {
                    "ok": True,
                    "message": "Data deleted",
                    "data": [{"rows_deleted": affected_rows}]
                }
            else:
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