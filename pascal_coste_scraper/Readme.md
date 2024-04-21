# Pascal Coste Web Scraper

## Introduction
This Python script is designed to scrape product data from the Pascal Coste website. It extracts information such as product names, prices, descriptions, URLs, and timestamps, and saves it into JSON. The data is then pushed to a database using a database script provided in `database.py`, which operates in a systematic manner.

## Requirements
- Python 3.x
- pandas
- BeautifulSoup (bs4)
- urllib
- sqlalchemy

## Installation
1. Ensure you have Python installed on your system.
2. Install the required dependencies using pip:

    ```
    pip install -r requirements.txt
    ```
3. Note that you need to provide your credentials in config.ini

## Functionality

### `main.py`

#### `url_data_extractor(url)`
Description: Extracts data from the provided URL using BeautifulSoup.
- Parameters:
  - url: The URL from which data is to be extracted.
- Returns: A BeautifulSoup object containing the parsed HTML content of the webpage.

#### `gather_next_page_links()`
Description: Finds and stores links to the next pages of products.
- Returns: None

#### `scrape_all_products()`
Description: Scrapes product data including name, image URL, brand, product URL, description, price, and timestamp.
- Returns: None

#### `main()`
Description: Main function to execute the scraping process.
- Returns: None

### `database.py`

#### Process Overview:
1. **Connection Establishment:** Establishes a connection to the specified database.
2. **Table Creation:** Checks if the required table exists in the database. If not, it creates the table based on the schema provided in the `tables.py` file.
3. **Data Insertion:** Reads data from the JSON file and inserts it into the database table.

This systematic process ensures efficient handling and storage of data within the specified database.

## Note:
- This script assumes a specific HTML structure of the Pascal Coste website. Any changes to the website's structure may require modifications to the code.

## Docker Setup and Execution.

### Startup Script

- The `startup.sh` script replaces placeholders in the `config.ini` file with the provided environment variables and then executes the Python application.

## Configuration

- Ensure that you set the required environment variables (`DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_DATABASE`, `DB_PORT`) when running the Docker container to configure the MySQL connection.

### Docker Commands
- docker pull amarkumar053/pascalrepo:pascalcoste_scraper_image
- docker run -d --name pascal_container -e DB_HOST=localhost -e DB_USER=DatabaseUserName -e DB_PASSWORD=DatabasePassword -e DB_DATABASE=DatabaseName -e DB_PORT=DatabasePort pascalcoste_scraper_image