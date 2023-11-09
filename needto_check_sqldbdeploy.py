#!/usr/bin/env vpython3
import os
import subprocess
import mysql.connector
import glob
import git

# Database connection parameters
db_params = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

#last_commit_sha = subprocess.check_output("git rev-parse HEAD", shell=True).decode("utf-8").strip()
#changed_files = glob.glob('mysql/*.sql')

# Iterate through the list of changed SQL files and print them
#for file in changed_files:
    #print(file)
    
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

#directory_path = "mysql/"
#try:
    #cursor.execute("START TRANSACTION")
# Use Git to get the list of changed SQL files
#git_command = git diff --name-only HEAD~1 HEAD -- '*.sql'

last_commit_sha = subprocess.check_output("git rev-parse HEAD", shell=True).decode("utf-8").strip()

print(f"last_commit: {last_commit_sha}")

git_command = f"git diff --name-only HEAD~1 {last_commit_sha} -- '*.sql'"
print(f"Executing command: {git_command}")
changed_files = subprocess.check_output(git_command, shell=True).decode("utf-8").strip().split("\n")

#changed_files = subprocess.check_output(git_command, shell=True).decode("utf-8").strip().split("\n")

#changed_files = subprocess.check_output(f"git diff --name-only HEAD~1 {last_commit_sha} -- '*.sql'", shell=True).decode("utf-8").strip().split("\n")
#changed_files = glob.glob('*.sql')

for file in changed_files:
    #script_path = os.path.join(directory_path, filename)

    with open(file, "r") as sql_file:
        sql_statements = sql_file.read().split(';')  # Split SQL statements by semicolon
        for sql_statement in sql_statements:
        # Execute the SQL statement against the database
            cursor.execute(sql_statement)
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
