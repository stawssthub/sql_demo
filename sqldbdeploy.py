
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
    

#directory_path = "mysql/"


# Use Git to get the list of changed SQL files
#git_command = git diff --name-only HEAD~1 HEAD -- '*.sql'
try:
    cursor.execute("START TRANSACTION")
    last_commit_sha = subprocess.check_output("git rev-parse HEAD", shell=True).decode("utf-8").strip()

    print(f"last_commit: {last_commit_sha}")

    git_command = f"git diff --name-only HEAD~1 {last_commit_sha} -- '*.sql'"

    print(f"Executing command: {git_command}")

#try:
    #cursor.execute("START TRANSACTION")
    changed_files = subprocess.check_output(git_command, shell=True).decode("utf-8").strip().split("\n")
    
    # Track executed statements
    executed_statements = set()
    
    # Execute the content of each modified SQL file
    for file in changed_files:
       with open(file, "r") as sql_file:
        #sql_statements = sql_file.read().split(';')  # Split SQL statements by semicolon
           #result_iterator = cursor.execute(sql_file.read(), multi=True)
            sql_script = (sql_file.read(), multi=True)
           # Split the script into statements
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]
            # Execute only new statements
            for stmt in statements:
                if stmt not in executed_statements:
                    cursor.execute(stmt)
                    executed_statements.add(stmt)
            
# commit the changes to the database 
    connection.commit()
except Exception as e:
    connection.rollback()
    print(f"Error: {e}")
finally:
# close the cursor and connection 
    cursor.close() 
    connection.close() 
