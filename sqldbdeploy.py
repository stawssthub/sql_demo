import os
import subprocess
import mysql.connector
import glob


def get_database_from_sql_file(mysql/):
    # Read the first few lines of the SQL file to find the database identifier
    with open(mysql/, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith('-- Database:'):
            return line.split(':')[1].strip()

    # If no database identifier is found, return None
    return None

def execute_sql_file_in_database(mysql/, database_config):
    try:
        connection = mysql.connector.connect(**database_config)
        cursor = connection.cursor()

        # Get the target database from the SQL file
        target_database = get_database_from_sql_file(mysql/)

        if target_database:
            # Use the specified database
            cursor.execute(f"USE {target_database}")

            # Read the SQL file and execute statements
            with open(mysql/, 'r') as file:
                sql_script = file.read()

            # Split SQL statements
            statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

            # Execute each statement
            for statement in statements:
                try:
                    cursor.execute(statement)
                    connection.commit()
                    print(f"Statement executed successfully in {target_database}: {statement}")
                except Exception as e:
                    print(f"Error executing statement in {target_database}: {statement}\nError: {e}")

    except mysql.connector.Error as err:
        print(f"Error connecting to database or executing SQL file: {err}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Specify your MySQL database configurations
db_params = [
    {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    },
    # Add more databases as needed
]

# Specify the directory containing your SQL files
sql_files_directory = 'mysql/'

# Get the SHA-1 hash of the latest commit
last_commit_sha = subprocess.check_output("git rev-parse HEAD", shell=True).decode("utf-8").strip()

# Get the list of changed SQL files
git_command = f"git diff --name-only HEAD~1 {last_commit_sha} -- '*.sql'"
changed_files = subprocess.check_output(git_command, shell=True).decode("utf-8").strip().split("\n")

# Deploy SQL files to each database
for db_config in db_params:
    for filename in changed_files:
        if filename.endswith(".sql"):
            sql_file_path = os.path.join(sql_files_directory, filename)
            execute_sql_file_in_database(sql_file_path, db_config)
