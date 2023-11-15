import os
import subprocess
import mysql.connector
import glob

# Database connection parameters
db_params = [
    {
        "host": "sql12.freesqldatabase.com",
        "port": "3306",
        "database": "sql12662061",
        "user": "sql12662061",
        "password": "lR7qTSsVuv",
    },
    {
        "host": "sql12.freesqldatabase.com",
        "port": "3306",
        "database": "sql12660740",
        "user": "sql12660740",
        "password": "srXYV5vv6M",
    },
    # Add more databases as needed
]

# Establish a database connection for each database
for db_config in db_params:
    try:
        connection = mysql.connector.connect(**db_config)
        print(f"\nConnected to database: {db_config['database']}")
        cursor = connection.cursor()

        # To get the list of databases
        cursor.execute("SHOW DATABASES")
        for database in cursor:
            print(f"Database: {database[0]}")

        # To get the list of tables in the database
        cursor.execute("SHOW TABLES")
        for table in cursor:
            print(f"Table: {table[0]}")

        # Commit the changes to the database
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error connecting to database: {db_config['database']}\nError: {err}")

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Get the list of changed SQL files
last_commit_sha = subprocess.check_output("git rev-parse HEAD", shell=True).decode("utf-8").strip()
print(f"Last commit: {last_commit_sha}")

git_command = f"git diff --name-only HEAD~1 {last_commit_sha} -- '*.sql'"
print(f"Executing command: {git_command}")

# Use Git to get the list of changed SQL files
changed_files = subprocess.check_output(git_command, shell=True).decode("utf-8").strip().split("\n")

# Establish a database connection for each changed file and execute SQL statements
for file in changed_files:
    try:
        with open(file, "r") as sql_file:
            sql_content = sql_file.read()

            # Extract the database name from the SQL content
            lines = sql_content.split("\n")
            for line in lines:
                if line.startswith("USE"):
                    database_name = line.split()[1].strip(";")
                    break
            else:
                raise ValueError("Database name not found in the SQL file.")

            # Find the database configuration based on the extracted database name
            db_config = next((config for config in db_params if config["database"] == database_name), None)
            if db_config is None:
                raise ValueError(f"Database configuration not found for database: {database_name}")

            # Connect to the database and execute SQL statements only if there are changes
            if db_config and file:
                connection = mysql.connector.connect(**db_config)
                print(f"\nConnected to database: {database_name}")
                cursor = connection.cursor()

                try:
                    cursor.execute("START TRANSACTION")
                    print(f"Executing SQL file: {file}")
                    result_iterator = cursor.execute(sql_content, multi=True)
                    print(result_iterator)
                    for res in result_iterator:
                        print("Running query: ", res)  # Will print out a short representation of the query
                        print(f"Affected {res.rowcount} rows")

                    connection.commit()
                    print("Execution complete")

                except Exception as e:
                    connection.rollback()
                    print(f"Error: {e}")

                finally:
                    cursor.close()
                    connection.close()

    except mysql.connector.Error as err:
        print(f"Error connecting to database or executing SQL file: {err}")

    except Exception as e:
        print(f"Error: {e}")
