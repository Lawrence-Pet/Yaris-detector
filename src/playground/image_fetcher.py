# This file uses the Programmable Search Engine from Google and the free tier API
# in order to fetch image URL's of the Yaris XP10. 

import requests, os, json
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(filename="image_fetcher.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()
API_KEY=os.getenv('GOOGLE_SEARCH_CLOUD_KEY')
CX = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
QUERY = "toyota yaris xp10"
PAGES = 50

items_list = []

logger.info(f"*** INITATING new query: {QUERY} for {PAGES} pages.")

for START in range (PAGES):
    url = f"https://www.googleapis.com/customsearch/v1?q={QUERY}&cx={CX}&searchType=image&key={API_KEY}&start={1+START*10}"
    logger.info(f"Page: {1+START*10}")
    response = requests.get(url).json()

    if "error" in response:
        logger.error(f"Error in response: {response['error']}")
        logger.debug(f"API Key: {API_KEY}")
        logger.debug(f"CX: {CX}")

    for item in response.get('items', []):
        items_list.append(item)

# Ends script if no items in itemlist
if len(items_list) == 0: 
    logger.warning("No items in itemlist.\n")
    exit()

logger.info(f"Counting {len(items_list)} results from query.\n")

output = {"items": items_list}
    
with open('response.json', 'w') as f:
    json.dump(output, f, indent=4)