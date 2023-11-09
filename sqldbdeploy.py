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

# Establish a database connection
connection = mysql.connector.connect(**db_params)
cursor = connection.cursor()

cursor.execute("SHOW DATABASES")

for D in cursor:
  print(D)
    
cursor.execute("SHOW TABLES")

for x in cursor:
  print(x)

# Step 1: Identify changed SQL files
changed_files = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD~1..HEAD', '--', '*.sql'], text=True).splitlines()

# Step 2: Execute changed SQL files
for file in changed_files:
    with open(file, 'r') as sql_file:
        sql_script = sql_file.read()
        cursor.execute(sql_script)
        connection.commit()

cursor.close()
connection.close()
