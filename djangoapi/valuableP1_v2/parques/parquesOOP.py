from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class ParquesOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()
    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self):
        cons="""
        INSERT INTO apm.parques 
            (description, area,geom)
        VALUES
            (%s,%s,
            st_geometryFromText(%s,%s))
        RETURNING id
        """
        self.cur.execute(cons,
                    ['My first park',
                    100,
                    'POLYGON ((728682.04891478247009218 4373483.63257919624447823, 728696.39738427905831486 4373525.62809967342764139, 728839.88207924494054168 4373479.08306447695940733, 728812.93495360505767167 4373402.09127693437039852, 728729.99380066129378974 4373451.08605082519352436, 728682.04891478247009218 4373483.63257919624447823))',
                    EPSG_CODE
                    ])
        self.conn.commit()
        l=self.cur.fetchall()
        #print(cur.fetchall()[0][0]) <-- ERROR. YOU ONLY CAN FECTH THE RESULTS ONCE
        print(l)
        print(l[0][0])
        self.disconnect()
        print("Inserted")

    def select(self, asDict=True):
        if asDict:
            #The rows are dicts
            self.cur=self.conn.cursor(row_factory=dict_row)
        
        cons="""
        SELECT 
            id, description, area, st_astext(geom)
        FROM 
            apm.parques 
        WHERE
            id>%s
        """
        self.cur.execute(cons, [0])
        l=self.cur.fetchall()
        print(l)
        print('First row:')
        print(l[0])
        self.disconnect()
        print("Selected")

    def update(self):
        cons="""
            UPDATE
                apm.parques 
            SET 
                (description, area, geom) = ROW(%s, %s, st_geometryFromText(%s,%s))    
            WHERE
                id>%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=['New description 2',200,'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))',EPSG_CODE, 0]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Updated")

    def delete(self):
        cons="""
            DELETE FROM
                apm.parques  
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=[6]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Deleted")

            
