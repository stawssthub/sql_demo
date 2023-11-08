import os
import mysql.connector
import glob

# Database connection parameters
db_params = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# Establish a database connection
connection = mysql.connector.connect(**db_params)
cursor = connection.cursor()

cursor.execute("SHOW DATABASES")

for D in cursor:
  print(D)
    
cursor.execute("SHOW TABLES")

for x in cursor:
  print(x)
    
#cursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
#cursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#cursor.execute("CREATE TABLE customers2 (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

# read the contents of the .sql file
with open('mysql/test_script.sql', 'r') as file: 
    sql_script = file.read()

# execute the script using the cursor object 
for result in cursor.execute(sql_script, multi=True): 
    pass 
 
# commit the changes to the database 
cnx.commit() 
 
# close the cursor and connection 
cursor.close() 
cnx.close() 
