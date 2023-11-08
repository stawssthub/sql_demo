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

cursor.execute("SHOW DATABASES")

for D in cursor:
  print(D)
    
cursor.execute("SHOW TABLES")

for x in cursor:
  print(x)
    
#cursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
#cursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#cursor.execute("CREATE TABLE customers2 (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

directory_path = "mysql/"
try:
    cursor.execute("START TRANSACTION")
# read the  .sql file
    for filename in os.listdir(directory_path):
        if filename.endswith(".sql"):
            script_paths = os.path.join(directory_path, filename)
            print(f"Processing: {script_paths}")
# Read the SQL script from the file
            with open(script_paths, 'r') as sql_file:
                result_iterator = cursor.execute(sql_file.read(), multi=True)
                print(result_iterator)
            for res in result_iterator:
                print("Running query: ", res)  # Will print out a short representation of the query
                print(f"Affected {res.rowcount} rows" )
 
# commit the changes to the database 
    connection.commit() 
except Exception as e:
    # Handle exceptions, roll back the transaction, and log the error
    connection.rollback()
    print(f"Error: {e}")
finally:
# close the cursor and connection 
    cursor.close() 
    connection.close() 
