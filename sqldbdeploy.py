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

# Function to execute SQL files
def execute_sql_files(directory):
    conn = mysql.connector.connect(**db_params)
    cursor = conn.cursor()

    for filename in os.listdir(directory):
        if filename.endswith(".sql"):
            with open(os.path.join(directory, filename), "r") as file:
                sql_script = file.read()
                cursor.execute(sql_script)

    conn.commit()
    conn.close()

# Example usage
execute_sql_files("mysql/") # Change directory path as needed
