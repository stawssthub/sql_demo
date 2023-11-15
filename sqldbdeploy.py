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

# Associate each SQL file with the corresponding database configuration dynamically
#sql_files_and_databases = {
    #file: db_params[i % len(db_params)] for i, file in enumerate(changed_files)
#}

sql_files_and_databases = {
    file: db_params[0] for file in changed_files  # Adjust the index as needed
}

# Establish a database connection for each changed file and execute SQL statements
for file, db_config in sql_files_and_databases.items():
    try:
        connection = mysql.connector.connect(**db_config)
        print(f"\nConnected to database: {db_config['database']}")
        cursor = connection.cursor()

        try:
            cursor.execute("START TRANSACTION")

            with open(file, "r") as sql_file:
                print(f"Executing SQL file: {file}")
                print(f"Target Database: {db_config.get('database', 'Unknown Database')}")
                result_iterator = cursor.execute(sql_file.read(), multi=True)
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

    finally:
        # Close the cursor and connection
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

        if 'connection' in locals() and connection.is_connected():
            connection.close()
