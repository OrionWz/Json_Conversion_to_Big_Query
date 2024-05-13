**README**

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

bash
Copy code
git clone https://github.com/your_username/your_repo.git
cd your_repo
Usage
Fetching Data
To fetch data from the API, run:

bash
Copy code
python fetch_data.py
Processing Data
To process the data and store it in a SQL table, run:

bash
Copy code
python process_data.py
Extracting to JSON
To extract the data to a JSON file, run:

bash
Copy code
python extract_to_json.py
Uploading to BigQuery
To upload the JSON file to BigQuery on Google Cloud, run:

bash
Copy code
python upload_to_bigquery.py
Configuration
You can configure the API URL, SQL table details, JSON file paths, and BigQuery credentials in the respective Python files.

