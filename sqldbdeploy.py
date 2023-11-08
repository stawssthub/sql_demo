import os
import subprocess
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

directory_path = "mysql/"
#try:
    #cursor.execute("START TRANSACTION")
# Use Git to get the list of changed SQL files
git_command = git diff --name-only HEAD~1 HEAD -- '*.sql'
changed_files = subprocess.check_output(git_command, shell=True).decode("utf-8").strip().split("\n")

for filename in changed_files:
    script_path = os.path.join(directory_path, filename)

    with open(script_path, 'r') as script_file:
        sql_script = script_file.read()
        
# commit the changes to the database 
    connection.commit() 
#except Exception as e:
    # Handle exceptions, roll back the transaction, and log the error
    #connection.rollback()
    #print(f"Error: {e}")
#finally:
# close the cursor and connection 
    cursor.close() 
    connection.close() 
