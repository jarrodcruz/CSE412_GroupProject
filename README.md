# CSE412_GroupProject

Our PostGreSQL web app.

## How to run:

1. Clone the GitHub repository
2. Create a database named 412_group_project on localhost port 5432
3. In the db, run the following to create a role with permissions to access the data:
      CREATE ROLE testuser WITH LOGIN PASSWORD '123';
4. Initialize the database using one of these options (DATABASE FILES folder):
      a. (Preferred) In pgAdmin, right click on 412_group_project, click “Restore…”, then select the Team42_db.backup file
      b. Run the Team42_db_nodata.sql file to initialize the schema, then manually import each .csv file (data folder) into each table with Delimiter = ‘,’ and Header Row = true. For the customers and employees tables specifically, add “NULL” as a null string.
      c. (Takes a LONG time) Using psql, manually run the Team42_db_long.sql file. This also automatically creates the database too.
5. Verify that all tables are imported, data is correctly populated, and permissions are successfully granted to role “testuser”
6. Run the following in a terminal where the repository was cloned to create an environment with the necessary packages:
      python3 -m venv .venv source .venv/bin/activate pip install -r requirements.txt
7. In the terminal with the packages installed, run the following:
      python app.py
8. Connect to localhost:4000 in a web browser
