import mysql.connector

dataBase = mysql.connector.connect(

    host= "localhost",
    user = 'root',
    passwd = 'youssef123'
)

#prepare a cursor object
cursorObject = dataBase.cursor()

#create a database

cursorObject.execute("CREATE DATABASE myDatabase")

print("all done")
