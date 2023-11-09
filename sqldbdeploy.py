
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

for file in changed_files:
    with open(file, "r") as sql_file:
        sql_statements = sql_file.read().split(';')  # Split SQL statements by semicolon
        for sql_statement in sql_statements:
        # Execute the SQL statement against the database
            cursor.execute(sql_statement)
            
# commit the changes to the database 
    connection.commit() 
    

# close the cursor and connection 
    cursor.close() 
    connection.close() 
