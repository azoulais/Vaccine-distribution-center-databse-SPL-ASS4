import sqlite3
import os
from Repository import repo


conn = sqlite3.connect('database.db')
repo.create_tables()
repo.configure()


with open("orders.txt") as input, open("output.txt", "w+") as output:
    for line in input.readlines():
        if line[-1]=='\n':
            line = line[:-1]

        params = line.split(',')
        if len(params)==3:
            repo.recieve_shipment(*params)
        else:
            repo.send_shipment(*params)

        output.write(repo.get_status() + "\r\n")
