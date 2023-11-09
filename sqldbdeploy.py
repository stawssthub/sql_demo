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

    changed_files = subprocess.check_output(['git', 'diff', '--name-only', 'HEAD^', 'HEAD'], universal_newlines=True)
    changed_files = [file.strip() for file in changed_files.split('\n') if file.endswith(".sql")]

    for file_path in changed_files:
        deploy_sql_changes(cursor, file_path)

    # Commit changes
    connection.commit()

cursor.close()
connection.close()
