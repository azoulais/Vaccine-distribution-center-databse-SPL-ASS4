import sqlite3
import atexit
from datetime import datetime

from DAOS import *
from DAOS import _Vaccines, _Suppliers, _Clinics, _Logistics


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def recieve_shipment(self, name, amount, date):
        amount = int(amount)
        id =self.vaccines.find_availiableId()
        supplier = self.suppliers.find_byName(name)
        self.insert_vaccine(id, date, supplier.id, amount)
        logistic_id = self.suppliers.find_byName(name).logistic
        self.logistics.add_count_received(logistic_id,amount)

    def send_shipment(self, location, amount):
        amount=int(amount)
        self.clinics.reduce_demand(location, amount)
        logistic_id = self.clinics.find(location).logistic
        while amount>0:
            oldest = self.vaccines.fetch_oldest()
            quan = oldest.quantity
            if quan>amount:
                self.logistics.add_count_sent(logistic_id,amount)
                self.vaccines.update_quantity(oldest.id,quan-amount)
            else:
                self.vaccines.delete(oldest.id)
                self.logistics.add_count_sent(logistic_id,oldest.quantity)

            amount -= oldest.quantity

    def get_status(self):
        return ",".join([str(self.vaccines.get_total_inventory()), str(self.clinics.get_total_demand()),
                         str(self.logistics.get_total_received()),str(self.logistics.get_total_sent())])





    def handle_orders(self, filepath):
        with open("orders.txt") as file:
            lines = file.readlines()
            for line in lines:
                params = line[:-1].split(',') if line[-1] == '\n' else line.split(',')
                if len(params) == 3:
                    repo.recieve_shipment(*params)
                else:
                    repo.send_shipment(*params)

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE logistics (
                id               INT        PRIMARY KEY,
                name             TEXT       NOT NULL,
                count_sent       INT        NOT NULL,
                count_received   INT        NOT NULL
            );
            CREATE TABLE clinics (
                id               INT        PRIMARY KEY,
                location         TEXT       NOT NULL,
                demand           INT        NOT NULL,
                logistic         INT                ,        
                FOREIGN KEY(logistic)    REFERENCES logistics(id)
            );
            CREATE TABLE suppliers (
                id               INT        PRIMARY KEY,
                name             TEXT       NOT NULL,
                logistic         INT                   ,
                FOREIGN KEY(logistic)    REFERENCES logistics(id)
            );
            CREATE TABLE vaccines(
            id                   INT        PRIMARY KEY,
            date                 DATE       NOT NULL,
            supplier             INT                ,
            quantity             INT        NOT NULL,
            FOREIGN KEY(supplier)        REFERENCES suppliers(id)
            );
    """)

    def configure(self):
        with open("config.txt") as file:
            numbers = file.readline()[:-1].split(',')

            vaccines = []
            for i in range(int(numbers[0])):
                vaccines.append(file.readline()[:-1])

            suppliers = []
            for i in range(int(numbers[1])):
                suppliers.append(file.readline()[:-1])

            clinics = []
            for i in range(int(numbers[2])):
                clinics.append(file.readline()[:-1])

            logistics = []
            for i in range(int(numbers[3]) - 1):
                logistics.append(file.readline()[:-1])
            logistics.append(file.readline())

            for line in logistics:
                params = line.split(',')
                repo.insert_logistic(*params)

            for line in clinics:
                params = line.split(',')
                repo.insert_clinic(*params)

            for line in suppliers:
                params = line.split(',')
                repo.insert_supplier(*params)

            for line in vaccines:
                params = line.split(',')
                repo.insert_vaccine(*params)

    def insert_vaccine(self, id, date, supplier, quantity):
        self.vaccines.insert(Vaccine(int(id),date, int(supplier), int(quantity)))

    def insert_supplier(self, id, name, logistic):
        self.suppliers.insert(Supplier(int(id), name, int(logistic)))

    def insert_clinic(self, id, location, demand, logistic):
        self.clinics.insert(Clinic(int(id), location, int(demand), int(logistic)))

    def insert_logistic(self, id, name, count_sent, count_received):
        self.logistics.insert((Logistic(int(id), name, int(count_sent), int(count_received))))


# the repository singleton
repo = _Repository()
atexit.register(repo._close)
