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

