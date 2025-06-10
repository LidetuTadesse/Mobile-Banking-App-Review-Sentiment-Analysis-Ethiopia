from google_play_scraper import Sort, reviews
import csv
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    filename='multi_bank_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# List of bank apps to scrape
BANK_APPS = {
    'Dashen Bank': 'com.dashen.dashensuperapp',
    'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',
    'Bank of Abyssinia': 'com.boa.boaMobileBanking'
}

def scrape_reviews(bank_name, app_id):
    logging.info(f"🔄 Fetching reviews for {bank_name}...")

    try:
        results, _ = reviews(
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=500  # You can increase this as needed
        )

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{bank_name.replace(" ", "_")}_reviews_{timestamp}.csv'

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['review_text', 'rating', 'date', 'bank_name', 'source'])
            writer.writeheader()

            for i, entry in enumerate(results, start=1):
                writer.writerow({
                    'review_text': entry['content'],
                    'rating': entry['score'],
                    'date': entry['at'].strftime('%Y-%m-%d'),
                    'bank_name': bank_name,
                    'source': 'Google Play'
                })

                if i % 50 == 0:
                    logging.info(f"✍️ {bank_name}: Written {i} reviews...")

        logging.info(f"✅ Saved {len(results)} reviews for {bank_name} to {filename}")

    except Exception as e:
        logging.error(f" Error fetching reviews for {bank_name}: {e}")
        print(f" Error with {bank_name}: {e}")

if __name__ == "__main__":
    for bank, app_id in BANK_APPS.items():
        scrape_reviews(bank, app_id)
