from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class CorredoresOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()
        
    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self):
        cons="""
        INSERT INTO apm.corredores 
            (description,dist,tipo,ancho,iluminacion,geom)
        VALUES
            (%s,%s,%s,%s,%s,
            st_geometryFromText(%s,%s))
        RETURNING id
        """
        self.cur.execute(cons,
                    ['My second corr',
                    120,
                    'peatonal',
                    2,
                    True,
                    'LINESTRING (728773.91411582741420716 4373270.24284076597541571, 727896.20773784175980836 4373567.71111082006245852)',
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
            id,description,dist,tipo,ancho,iluminacion,st_astext(geom)
        FROM 
            apm.corredores 
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
                apm.corredores 
            SET 
                (description,dist,tipo,ancho,iluminacion, geom) = ROW(%s,%s,%s,%s,%s, st_geometryFromText(%s,%s))    
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=['My second corr',
                    120,
                    'ciclovia',
                    1.5,
                    True,
                    'LINESTRING (728773.91411582741420716 4373270.24284076597541571, 727896.20773784175980836 4373567.71111082006245852)',
                    EPSG_CODE,
                    3
                    ]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Updated")

    def delete(self):
        cons="""
            DELETE FROM
                apm.corredores  
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=[1]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Deleted")

            
