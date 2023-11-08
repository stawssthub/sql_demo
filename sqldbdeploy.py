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

cursor.execute(mysql/test_script.sql)
