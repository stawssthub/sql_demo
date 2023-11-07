import os
import mysql.connector
import glob

# Database connection parameters
databases = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

# Function to execute SQL files for a specific database
def execute_sql_files(directory, database):
    connection = mysql.connector.connect(
        host=database["host"],
        user=database["user"],
        password=database["password"],
        database=database["name"]
    )

    cursor = connection.cursor()

    for filename in os.listdir(directory):
        if filename.endswith(".sql"):
            with open(os.path.join(directory, filename), "r") as file:
                sql_script = file.read()
                cursor.execute(sql_script)

    connection.commit()
    connection.close()

# Example usage
for db in databases:
    execute_sql_files("sql_scripts/schema/", db) # Change directory path as needed
