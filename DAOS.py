from DTOS import *


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
                       INSERT INTO vaccines (id, date,supplier, quantity) VALUES (?,?,?,?)
                   """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, date, supplier, quantity FROM vaccines WHERE id = ?
        """, [vaccine_id])
        return Vaccine(*c.fetchone())

    def fetch_oldest(self):
        c = self._conn.cursor()
        c.execute("""
                    SELECT id, date, supplier, quantity FROM vaccines ORDER BY date ASC
                """)
        return Vaccine(*c.fetchone())

    def delete(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            DELETE FROM vaccines WHERE id = ?
        """, [vaccine_id])

    def update_quantity(self,vaccine_id, new_quantity):
        c = self._conn.cursor()
        c.execute("""
            UPDATE vaccines SET quantity=? WHERE id = ?
        """, [new_quantity,vaccine_id])


    def get_total_inventory(self):
        c=self._conn.cursor()
        c.execute("""
                  SELECT SUM(quantity) FROM vaccines  
        """)
        return c.fetchone()[0]

    def find_availiableId(self):
        c = self._conn.cursor()
        c.execute("""
            SELECT id FROM vaccines ORDER BY id ASC;
        """)
        next = c.fetchone()
        i = 1
        while next != None and next[0] == i:
            i+=1
            next= c.fetchone()

        return i

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                  INSERT INTO suppliers (id, name,logistic) VALUES (?,?,?)
                 """, [supplier.id, supplier.name, supplier.logistic])

    def find_byName(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, logistic FROM suppliers WHERE name = ?
        """, [supplier_name])
        return Supplier(*c.fetchone())

    def find_byId(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, logistic FROM suppliers WHERE id = ?
        """, [supplier_id])
        return Supplier(*c.fetchone())

class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
                   INSERT INTO clinics (id, location,demand,logistic) VALUES (?,?,?,?)
                """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_location):
        c = self._conn.cursor()
        c.execute("""
                    SELECT id, location,demand, logistic FROM clinics WHERE location = ?
                """, [clinic_location])
        return Clinic(*c.fetchone())

    def reduce_demand(self, clinic_location, number_toReduce):
        new_demand=self.find(clinic_location).demand - number_toReduce
        c = self._conn.cursor()
        c.execute("""
            UPDATE clinics SET demand=? WHERE location = ?
        """, [new_demand,clinic_location])

    def get_total_demand(self):
        c=self._conn.cursor()
        c.execute("""
                  SELECT SUM(demand) FROM clinics  
        """)
        return c.fetchone()[0]


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
                    INSERT INTO logistics (id, name,count_sent,count_received) VALUES (?,?,?,?)
                 """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
                    SELECT id, name,count_sent, count_received FROM logistics WHERE id = ?
                """, [logistic_id])
        return Logistic(*c.fetchone())

    def add_count_received(self, logistic_id, number_toAdd):
        new_count=self.find(logistic_id).count_received + number_toAdd
        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_received=? WHERE id = ?
        """, [new_count,logistic_id])

    def add_count_sent(self, logistic_id, number_toAdd):
        new_count=self.find(logistic_id).count_sent + number_toAdd
        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_sent=? WHERE id = ?
        """, [new_count,logistic_id])

    def get_total_received(self):
        c=self._conn.cursor()
        c.execute("""
                  SELECT SUM(count_received) FROM logistics  
        """)
        return c.fetchone()[0]

    def get_total_sent(self):
        c=self._conn.cursor()
        c.execute("""
                  SELECT SUM(count_sent) FROM logistics  
        """)
        return c.fetchone()[0]

