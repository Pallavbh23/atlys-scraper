# FastAPI Scraping Tool

## Project Overview

This project is a web scraping tool built as a project for Atlys with FastAPI to automate the extraction of product information from [dentalstall.com](https://dentalstall.com/shop/). The tool scrapes product names, prices, and images from the catalogue and caches the results using Redis.

## Features

1. **Scraping**:
    - Scrapes product details (name, price, and image) from the catalogue pages.
    - Optional settings to limit the number of pages to scrape and to use a proxy.
  
2. **Caching**:
    - Utilizes Redis to cache scraped data for 5 minutes to reduce redundant requests and improve performance.
  
3. **Persistence**:
    - Stores the scraped data in JSON format locally.
  
4. **Notification**:
    - Prints the number of scraped and updated products to the console after each scraping session.
  
5. **Authentication**:
    - Simple token-based authentication for the scraping endpoint.
  
6. **Logging**:
    - Logs cache hits, misses, and errors during the scraping process.


## Installation

1. Clone the repository:
```sh
   git clone <repository_url>
   cd project
```

2. Set up a virtual environment:

```sh
python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```sh
pip install -r requirements.txt
```

4. Create a .env file with the following content:


```sh
STATIC_TOKEN=your_static_token
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_CACHE_TIMEOUT=300
```

5. Start a Redis server. You can use Docker for quick setup:

```sh
docker run --name redis -p 6379:6379 -d redis
```

6. Running the Application

Start the FastAPI application:

```sh
uvicorn app.main:app --reload
```
7. Make a POST request to the /extract-products endpoint with the required token for authentication.

Example Request:

```sh
curl --location 'http://127.0.0.1:8000/extract-products' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer statictokenatlys' \
--data '{
    "pages": 6,
    "proxy": "http://your_proxy_url"
}'

```


## Why BeautifulSoup?
BeautifulSoup was chosen over Selenium for this project due to the following reasons:

* Performance: BeautifulSoup is generally faster than Selenium for tasks that do not require JavaScript execution. Since the target website's product information is available in the HTML, BeautifulSoup can parse it directly without the overhead of browser automation.

* Resource Usage: BeautifulSoup uses significantly fewer system resources compared to Selenium, which requires running a full web browser.

* Simplicity: BeautifulSoup's API is straightforward for parsing and extracting data from HTML, making it a better fit for this project's requirements.

## Implemented Features
* Scraping: Extracts product titles, prices, and images from the catalogue pages.
* Caching: Uses Redis to cache the results of scraped pages for 5 minutes.
Error Handling: Includes basic error handling and retry mechanisms for network requests.
* Logging: Logs various events and errors during the scraping process.
Configuration: Reads configuration from a .env file for easy customization.
* Authentication: Simple token-based authentication for securing the API endpoint.
* Notification: Prints the number of scraped products to the console after each run.


# Future Improvements

* Add support for different storage backends (e.g., databases).
* Implement more sophisticated notification methods (e.g., email, Slack).
* Add more configuration options and improve flexibility.