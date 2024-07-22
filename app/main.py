from fastapi import FastAPI, Depends, Request
from app.schemas import ScrapeSettings
from app.scraper import Scraper
from app.utils import download_image
from app.database import crud
from app.dependencies import verify_token

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler('main.log'),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

# Initialize logger
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/extract-products", dependencies=[Depends(verify_token)])
async def extract_products(settings: ScrapeSettings):
    scraper = Scraper(base_url="https://dentalstall.com/shop/", proxy=settings.proxy)
    products = scraper.scrape(pages=settings.pages)
    try:
        update_count = 0
        for product in products:
            product['path_to_image'] = download_image(product['path_to_image'])
            updated = crud.update_product(product)
            if updated:
                update_count += 1
        logger.info(f'Updated {update_count} products')
    except Exception as e:
        logger.log(e)

    scraped_count = len(products)
    print(f"{scraped_count} products were scraped and updated in the database.")

    return {"scraped_count": scraped_count, "products": products}