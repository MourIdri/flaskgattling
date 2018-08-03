import sys
import os
import logging
import time
import datetime
import json
import uuid
import requests
import ast
from flask import Flask, request , render_template
from werkzeug import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from flask_restful import Resource, Api
import json, sys, ast




import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)

app = Flask(__name__)
api = Api(app)
app.debug = True


def GetConfig ():
    with open("credentials.json", 'r') as f:
        data = json.loads(f.read())
        global mysqlhost
        global mysqluser
        global mysqlpassword
        global mysqldatabase
        global mysqldatabasetable
        mysqlhost = data["azuremysql"]["host"]
        mysqluser = data["azuremysql"]["user"]
        mysqlpassword = data["azuremysql"]["password"]
        mysqldatabase = data["azuremysql"]["database"]
        mysqldatabasetable = data["azuremysql"]["table_name"]
        return mysqlhost,mysqluser,mysqlpassword,mysqldatabase,mysqldatabasetable


#Getting logging information for DB 
GetConfig ()

# Obtain connection string information from the portal
config = {
  'host':mysqlhost,
  'user':mysqluser,
  'password':mysqlpassword,
  'database':mysqldatabase,
}
#provide the name of the table
table_name = mysqldatabasetable
#Create Connexion and cursor :
conn = mysql.connector.connect(**config)
cursor = conn.cursor(buffered=True)



def drop_table_fi_existe ():
    #Drop previous table of same name if one exists
    cursor.execute("DROP TABLE IF EXISTS %s;") % (table_name)
    print("*** DEBUG FUNCTION drop_table_fi_existe finished dropping table (if existed).")

def create_if_not_exist(columns_mysql_db_keys):
    createsqltable = """CREATE TABLE IF NOT EXISTS """ + table_name + " (id serial PRIMARY KEY, " + " VARCHAR(150), ".join(columns_mysql_db_keys) + " VARCHAR(150)) ;"
    cursor.execute(createsqltable)
    print("*** DEBUG FUNCTION create_if_not_exist Finished creating table.")


def insert_some_data(query_columns,query_placeholders,columns_mysql_db_values):
    insert_query_bis = """INSERT INTO """ + table_name + "(" +query_columns +") VALUES ("+query_placeholders+");"
    cursor.execute(insert_query_bis, columns_mysql_db_values)
    print("*** DEBUG FUNCTION insert_some_data Inserted",cursor.rowcount,"row(s) of data.")


def read_some_data():
    read_query_bis = """SELECT * FROM """ + table_name + " ;"
    cursor.execute(read_query_bis)
    rows = cursor.fetchall()
    print("*** DEBUG FUNCTION Read",cursor.rowcount,"row(s) of data.")
    # Print all rows
    #for row in rows:
        #debug_message_0 = "*** DEBUG FUNCTION Data row = ("+Rows_var_placeholders+")"
        #print"*** DEBUG FUNCTION Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2]))
    widths = []
    columns = []
    tavnit = '|'
    separator = '+'
    for cd in cursor.description:
        widths.append(max(cd[2], len(cd[0])))
        columns.append(cd[0])
    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'
    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in rows:
        print(tavnit % row)
    print(separator)
    print("*** DEBUG FUNCTION read_some_data Finished read table.")


def search_data_fromDB (keyword_STRUserUUID1):
    search_query_bis = "SELECT distinct * FROM `%s` WHERE STRUserUUID1 LIKE '%s' ; " % (table_name,keyword_STRUserUUID1)
    cursor.execute(search_query_bis)
    rows = cursor.fetchall()
    #print rows
    #read
    widths = []
    columns = []
    tavnit = '|'
    separator = '+'
    for cd in cursor.description:
        widths.append(max(cd[2], len(cd[0])))
        columns.append(cd[0])
    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'
    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in rows:
        print(tavnit % row)
    print(separator)
    print("*** DEBUG FUNCTION search_data_fromDB Finished Search table.")



request_stdin = json.load (sys.stdin)
print "\n*** DEBUG test_myscript.py  request is %s " %(request_stdin)
strMetdatasFromJSON0_stdin = str(request_stdin)
MetdatasDICT_stin = ast.literal_eval(strMetdatasFromJSON0_stdin)
for key in MetdatasDICT_stin :
    print "key: %s , value: %s" % (key, MetdatasDICT_stin[key])
    STRUserUUID1 = MetdatasDICT_stin["STRUserUUID1"]
    keyword = STRUserUUID1
print "\n*** DEBUG db_operations_v9_read.py  request is %s " %(MetdatasDICT_stin)
print "\n*** DEBUG db_operations_v9_read.py  request is %s " %(keyword)



#now store data in a MysqlDatabase
datas = MetdatasDICT_stin
#Creating a list from the Keys of the dictionnary and a series of %s with same number of values
columns_mysql_db_keys = datas.keys()
columns_mysql_db_values = datas.values()
query_placeholders = ", ".join(["%s"] * len(columns_mysql_db_values))
query_columns = ", ".join(columns_mysql_db_keys)
query_columns_values = ", ".join(columns_mysql_db_values)
print query_placeholders
print query_columns
print query_columns_values
# Construct connection string
mysql.connector.connect() # For testing..
try:
    conn
    cursor
    print "*** DEBUG FUNCTION Connection established"
    #Drop table if existe (optionnal )
    #drop_table_fi_existe ()
    # Create table if no existe
    #create_if_not_exist(columns_mysql_db_keys)
    # Insert some data into table
    #insert_some_data(query_columns,query_placeholders,columns_mysql_db_values)
    # Read data
    read_some_data()
    search_data_fromDB (keyword)
    # Cleanup
    conn.commit()
    cursor.close()
    conn.close()
except mysql.connector.Error as err:
    print "*** DEBUG FUNCTION Connection COULD NOT BE established"
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print "*** DEBUG FUNCTION Something is wrong with the user name or password"
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print "*** DEBUG FUNCTION Database does not exist"
    else:
        print "*** DEBUG FUNCTION Database err message "
        print "*** DEBUG FUNCTION Database issue is  : ... ", err
        if err == "Cursor is not connected":
            cursor
            pass
        if err == "2013 (HY000): Lost connection to MySQL server during query":
            conn
            cursor
            pass
        if err == "2006 (HY000): MySQL server has gone away":
            print "*** DEBUG FUNCTION Database... Try to reconnect "
            conn
            cursor
            pass
        pass
else:
    print("*** DEBUG FUNCTION customerrequest Done.")
    pass

print "*** DEBUG FUNCTION This process has the pid", os.getpid()