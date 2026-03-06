from psycopg.rows import dict_row
from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE,SNAPTOGRIDDEC
from myLib.database import Database as Db


class Trees(Db):
    def __init__(self):
        super().__init__()

    def insert(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'])
        Db.insert(self,'apm.trees',dict)
        
        
        # cons="""
        # INSERT INTO apm.trees 
        #     (description,species,height,condition,is_protected,geom)
        # VALUES
        #     (%s,%s,%s,%s,%s,
        #     st_snaptogrid(st_geometryFromText(%s,%s),%s))
        # RETURNING id
        # """
        # try:
        #     self.cur.execute(cons,
        #                 [dict['description'],
        #                 dict['species'],
        #                 dict['height'],
        #                 dict['condition'],
        #                 dict['is_protected'],
        #                 dict['geom'],
        #                 EPSG_CODE,
        #                 SNAPTOGRIDDEC
        #                 ])
        #     self.conn.commit()
        #     l=self.cur.fetchall()
        #     self.disconnect()
        #     print("Inserted")
        #     print([{"id":l[0][0]}])
        #     self.disconnect()
        #     return {
        #         "ok": True,
        #         "message": "Data inserted",
        #         "data": [{"id":l[0][0]}]}
        # except Exception as e:
        #         print(f'Error:{e}')
        #         self.conn.rollback()
        #         self.disconnect()
        #         return {
        #             "ok": False,
        #             "message": str(e),
        #             "data": None
        #             }

    def select(self, dict, asDict=False):
        fields = 'id,description,species,height,condition,is_protected,st_astext(geom)'
        Db.select(self,'apm.trees',fields,dict['id'],asDict)

    def update(self,dict):
        Db.is_valid(self,dict['geom'])
        Db.check_intersection(self,dict['geom'],id=dict['id'],command='update')
        cons="""
            UPDATE
                apm.trees 
            SET 
                (description,species,height,condition,is_protected,geom) = ROW(%s, %s,%s,%s,%s, st_snaptogrid(st_geometryFromText(%s,%s),%s))    
            WHERE
                id=%s
            """
        valuesList=[dict['description'],
                        dict['species'],
                        dict['height'],
                        dict['condition'],
                        dict['is_protected'],
                        dict['geom'],
                        EPSG_CODE,
                        SNAPTOGRIDDEC,
                        dict['id']
                        ]
        try:
            self.cur.execute(cons, valuesList)
            affected_rows = self.cur.rowcount
            self.conn.commit()
            if affected_rows > 0:
                print(f'rows_updated:{affected_rows}')
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
        Db.delete(self,table='apm.trees',id=dict['id'])
