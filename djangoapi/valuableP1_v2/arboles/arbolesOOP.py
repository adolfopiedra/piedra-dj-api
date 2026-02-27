from psycopg.rows import dict_row

from myLib.connect import connect
from myLib.p1Settings import EPSG_CODE


class ArbolesOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def insert(self):
        cons="""
        INSERT INTO apm.trees 
            (description,species,height,condition,is_protected,geom)
        VALUES
            (%s,%s,%s,%s,%s,
            st_geometryFromText(%s,%s))
        RETURNING id
        """
        self.cur.execute(cons,
                    ['My secind tree',
                    'Manzano',
                    10,
                    'Bueno',
                    True,
                    'POINT (728926.0603868915932253 4373197.45060526859015226)',
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
            id, description,species,height,condition,is_protected,st_astext(geom)
        FROM 
            apm.trees 
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
                apm.trees 
            SET 
                (description,species,height,condition,is_protected,geom) = ROW(%s, %s,%s,%s,%s, st_geometryFromText(%s,%s))    
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=['My second tree',
                    'Manzano',
                    10,
                    'Bueno',
                    True,
                    'POINT (728926.0603868915932253 4373197.45060526859015226)',
                    EPSG_CODE,
                    8
                    ]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Updated")

    def delete(self):
        cons="""
            DELETE FROM
                apm.trees  
            WHERE
                id=%s
            """
        # As there are 5 %s, you need a list with 5 values: 
        #   [description, area, the_geom_wkt, the_epsg_code, 
        #           the_id_to_select_the_row]
        valuesList=[5]
        self.cur.execute(cons, valuesList)
        print(self.cur.rowcount)
        self.conn.commit()
        self.disconnect()
        print("Deleted")