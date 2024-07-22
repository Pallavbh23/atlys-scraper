import logging
import httpx
from bs4 import BeautifulSoup
from app.redis_client import redis_client
from app.config import settings
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler('scraper.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Initialize logger
logger = logging.getLogger(__name__)
class Scraper:
    def __init__(self, base_url, proxy=None):
        self.base_url = base_url
        self.proxy = proxy
        self.session = httpx.Client(proxies=self.proxy)

    def scrape_page(self, page_num):
        cache_key = f"page_{page_num}"
        
        # Check Redis cache
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info(f"Cache hit for page {page_num}")
            return json.loads(cached_data)
        if page_num != 1:
            url = f"{self.base_url}page/{page_num}/"
        else:
            url = self.base_url
        response = self.session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return self.extract_products(soup, cache_key)
        else:
            retry_count = 0
            while retry_count < 3 and response.status_code !=200:
                response = self.session.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    return self.extract_products(soup, cache_key)
                else :
                    retry_count += 1
                    logger.info(f"Failed to fetch page {page_num}, retrying...")
            logger.error(f"Failed to fetch page {page_num}, maximum retries exceeded")
            
        return []

    def extract_products(self, soup, cache_key):
        try:
            products = soup.select('div.product-inner')
            all_data = []

            # Iterate over each product and extract details
            for product in products:
                # Extract product name
                product_name = product.select_one('h2.woo-loop-product__title a').get_text(strip=True)

                # Extract product image URL
                product_image = product.select_one('div.mf-product-thumbnail img')['data-lazy-src']

                # Extract product prices
                price_container = product.select_one('span.price')
                
                # Check if current price exists
                current_price_element = price_container.select_one('ins span.woocommerce-Price-amount') if price_container else None
                current_price = current_price_element.get_text(strip=True) if current_price_element else 'N/A'
                
                if current_price == 'N/A':
                    current_price_element = product.select_one('span.woocommerce-Price-amount', "")
                    current_price = current_price_element.get_text(strip=True) or 'N/A'

                all_data.append(
                    {
                    "product_title":product_name,
                    "product_price":current_price,
                    "path_to_image":product_image, # path to image at your PC
                    }
                )
            redis_client.setex(cache_key, settings.redis_cache_timeout, json.dumps(all_data))
            logger.info(f"Cached page {cache_key} data")
            return all_data
        except Exception as e:
            print(e)
            logger.error(e)

    def scrape(self, pages=1):
        all_products = []
        for page in range(1, pages + 1):
            all_products.extend(self.scrape_page(page))
        return all_products