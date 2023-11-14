import os
import subprocess
import mysql.connector
import glob

def get_latest_commit_sha():
    # Use Git to get the SHA-1 hash of the latest commit
    last_commit_sha = subprocess.check_output("git rev-parse HEAD", shell=True).decode("utf-8").strip()
    return last_commit_sha

def get_changed_files_since_commit(commit_sha):
    # Use Git to get the changed files since the specified commit
    git_command = f"git diff --name-only {commit_sha} HEAD"
    changes = subprocess.check_output(git_command, shell=True, universal_newlines=True)
    return changes.strip().split('\n')

def execute_sql_file(mysql, connection):
    try:
        # Read SQL file
        with open(mysql, 'r') as file:
            sql_script = file.read()

        # Split SQL statements
        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

        # Create a cursor and execute SQL statements
        cursor = connection.cursor()
        for statement in statements:
            try:
                cursor.execute(statement)
                connection.commit()
                print(f"Statement executed successfully: {statement}")
            except Exception as e:
                print(f"Error executing statement: {statement}\nError: {e}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def deploy_to_databases(database_configurations, mysql):
    # Get the SHA-1 hash of the latest commit
    last_commit_sha = get_latest_commit_sha()

    # Get the changed files since the last commit
    changed_files = get_changed_files_since_commit(last_commit_sha)

    for db_config in database_configurations:
        try:
            # Connect to the database
            connection = mysql.connector.connect(**db_config)
            print(f"\nConnected to database: {db_config['database']}")

            # Loop through each changed SQL file
            for filename in changed_files:
                if filename.endswith(".sql"):
                    sql_file_path = os.path.join(mysql, filename)
                    print(f"\nExecuting SQL file: {sql_file_path}")
                    execute_sql_file(sql_file_path, connection)

        except mysql.connector.Error as err:
            print(f"Error connecting to database: {db_config['database']}\nError: {err}")

        finally:
            # Close the connection
            if connection.is_connected():
                connection.close()
                print(f"Disconnected from database: {db_config['database']}")

if __name__ == "__main__":
    # Specify your MySQL database configurations
  database_configurations = [{
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
},
{
    "host": os.getenv("DB_HOST_2"),
    "port": os.getenv("DB_PORT_2"),
    "database": os.getenv("DB_NAME_2"),
    "user": os.getenv("DB_USER_2"),
    "password": os.getenv("DB_PASSWORD_2"),
},
]

    # Specify the directory containing your SQL files
    sql_files_directory = 'mysql/'

    # Deploy SQL files to each database
    deploy_to_databases(database_configurations, sql_files_directory)
