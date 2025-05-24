Multicultural User Data Project README
Hey there! Welcome to the Multicultural User Data Project. This is a small but mighty setup for managing user data, multicultural demographics, and pulling in some external API data for fun. It’s built with SQL for database operations and Python for handling API calls and JSON file processing. Below, I’ll break down what’s going on, how to set it up, and what each piece does.

What’s This Project About?
This project does a few things:

Stores and queries user data (names, gender, age) in a PostgreSQL database.
Manages multicultural data (occupation, ethnicity, location) in a separate table.
Joins the two tables to analyze combined data.
Pulls data from an external API (in this case, Nintendo Switch games) and saves it as JSON.
Processes JSON files using Python and Prefect for workflow orchestration.
It’s a mix of database management and data processing, perfect for learning SQL, Python, and data workflows or building a small analytics tool.

Prerequisites
Before you dive in, make sure you have:

PostgreSQL: For the database. Install it and set up a database instance.
Python 3.8+: For running the Python scripts.
Python Libraries:
requests (for API calls)
prefect (for workflow orchestration)
Install them with: pip install requests prefect
A text editor or IDE (VS Code, PyCharm, etc.).
Access to the internet for the API calls.
Setup Instructions
Set Up the Database:
Create a PostgreSQL database (e.g., multicultural_db).
Run the SQL scripts in sql_scripts/ to create the tables:
data_users: Stores user info (ID, first name, last name, gender, age).
MulticulturalData: Stores cultural info (ID, occupation, ethnicity, state/city).
Example SQL to create the data_users table:
sql

Copy
CREATE TABLE data_users (
    data_users_id SERIAL PRIMARY KEY,
    First_Name VARCHAR(100),
    Last_Name VARCHAR(100),
    Gender VARCHAR(100),
    Age INT
);
Do the same for MulticulturalData and run the INSERT statements to add sample data.
Run the SQL Queries:
Use a tool like pgAdmin or the psql command line to execute queries.
The SQL scripts include:
Selecting all users (SELECT * FROM data_users).
Filtering by gender and age (e.g., females or males 60+).
Grouping by gender or age for counts.
Finding names starting with ‘A’ or ages between 18–25.
Joining data_users and MulticulturalData on data_users_id = Culture_id.
Check the SQL files for the full list.
Set Up the Python Environment:
Clone this repo or copy the Python scripts to your machine.
Install dependencies: pip install requests prefect.
Update file paths in the Python scripts (e.g., C:\Users\banks\OneDrive\Documents\nell_file.json) to match your local setup.
Run the Python Scripts:
API Data Fetching:
The script in fetch_api.py pulls Nintendo Switch game data from https://api.sampleapis.com/switch/games.
It saves the data to output.json.
Run it with: python fetch_api.py.
JSON Processing:
The process_json.py script uses Prefect to read a JSON file, process it (converts records to JSON strings), and write to a new file.
Update the file_path_in and file_path_out variables to your JSON file paths.
Run it with: python process_json.py.
There’s also a simpler simple_json.py script that does similar JSON processing without Prefect.
Note: One script has an incomplete file path (C:\). Update it to a valid path before running.
What’s in the Code?
SQL
Tables:
data_users: Basic user info with a serial ID as the primary key.
MulticulturalData: Cultural details tied to users via Culture_id.
Queries:
Insert/delete sample data (e.g., adding ‘Jurema’ and deleting her).
Filter users by gender, age, or name patterns.
Aggregate data (e.g., count users by gender or age).
Join tables to combine user and cultural data.
Sample Query:
sql

Copy
SELECT * FROM data_users
INNER JOIN MulticulturalData
ON data_users.data_users_id = MulticulturalData.Culture_id;
Python
API Fetching:
Uses requests to grab data from a public API.
Saves it as formatted JSON using json.dumps.
JSON Processing:
Two approaches: a Prefect workflow and a standalone script.
Both read JSON, convert records to strings, and write to a new file.
Sample Code:
python

Copy
def fetch_api_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None
Known Issues
The INSERT statement for data_users is missing column names:
sql

Copy
insert into data_users values(200, 'Jurema', 'Campos', 'female', 35);
Fix it by specifying columns:
sql

Copy
INSERT INTO data_users (data_users_id, First_Name, Last_Name, Gender, Age)
VALUES (200, 'Jurema', 'Campos', 'female', 35);
The MulticulturalData INSERT has an empty values() clause. Remove or complete it.
One Python script has an incomplete file path. Update it to avoid errors.
The API URL is public, but if it goes down, you’ll need a backup API.
Next Steps
Add more sample data to test queries.
Expand the SQL queries to include more analytics (e.g., average age by ethnicity).
Enhance the Python scripts to handle larger JSON files or different APIs.
Add error handling for file paths and API failures.
Maybe throw in a front-end to visualize the data (e.g., a simple Flask app).
Contributing

















































**README**


User
Task:
Your task is to create a Python application that extracts data from the RandomUser API (https://randomuser.me/api/) and gathers a dataset of 200 or more items. Next, use one of the following APIs (or another interesting one of your choice) to infer more information about the names within the random name file: https://nationalize.io/, https://genderize.io/, https://agify.io/. 
 
Finally, use SQL to perform 5 or more queries on the dataset that you think might yield interesting results. Feel free to explore and be creative with your queries.
 
Requirements:
Use Python to fetch data from the RandomUser API.
Use an additional API to infer more information about the names within the dataset.
Use SQL to perform at least 5 interesting queries on the name file dataset.
Ensure your code is well-structured, documented, and follows best practices.
 
Submission:
Upload your application and any other relevant files to github, make sure to include a README with instructions on how to run your application and any relevant details. 
How you store the data or not is up to you.
 
Additionally, include a brief explanation of your approach and any interesting insights you gained from your analysis.
 
Note: 
You are encouraged to use any Python libraries that may help you complete the task efficiently.
Remember that we are looking for a well-structured and efficient solution that showcases your Python and SQL skills.
Feel free to reach out if you have any questions about the test. We look forward to reviewing your submission






**Project Description:**
This project, completed as part of a take-home assignment for the Detroit Lions, involves the development of Python scripts and SQL queries for data manipulation and analysis. I created the fetcher to fetch data from a random api and I stored that data in a data base & made 5 interesting queries in SQL about the 200 people from that random API. Then i converted my json file to big query on google cloud.

Data Fetcher and Processor
This project fetches data from an API, stores it in a SQL table, extracts it to a JSON file, and uploads it to BigQuery on Google Cloud.

Prerequisites
Python 3.x
requests library (pip install requests)
Prefect (pip install prefect)
Installation
Clone the repository:


Usage
Fetching Data
To fetch data from the API, run:

python fetch_data.py
Processing Data
To process the data and store it in a SQL table, run:


python process_data.py
Extracting to JSON
To extract the data to a JSON file, run:


python extract_to_json.py
Uploading to BigQuery
To upload the JSON file to BigQuery on Google Cloud, run:


python upload_to_bigquery.py
Configuration
You can configure the API URL, SQL table details, JSON file paths, and BigQuery credentials in the respective Python files.

