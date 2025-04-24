# CSE412_GroupProject

Our PostGreSQL web app.

## How to run:

### Setup the Database:

1. Open pgAdmin
2. Create the database '412_group_project'
3. Create the following user:

   CREATE ROLE testuser WITH LOGIN PASSWORD '123';



### Setup Environment:

1. Run the following in a terminal to create an environment with the necessary packages:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

### Run the backend:

1. In a terminal with the packages installed, run the following:

python app.py
