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
    conn = mysql.connector.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
