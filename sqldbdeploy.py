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

# Directory containing SQL scripts
sql_script_dir = "hawthorn"  # Replace with your actual directory path

# Get a list of all SQL files in the directory
sql_files = glob.glob(os.path.join(sql_script_dir, "**.sql"))

# Check if a script has already been deployed and deploy if not
for script in sql_files:
    script_name = os.path.basename(script)
    cursor.execute("SELECT script_name FROM deployed_scripts WHERE script_name = %s", (script_name,))
    if not cursor.fetchone():
        with open(script, "r") as file:
            sql = file.read()
        cursor.execute(sql)
        cursor.execute("INSERT INTO deployed_scripts (script_name) VALUES (%s)", (script_name,))

# Commit the changes and close the connection
connection.commit()
cursor.close()
connection.close()
