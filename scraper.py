import time
from datetime import datetime, timedelta
import uuid
import argparse

from helium import start_chrome, write, S, click, find_all, kill_browser
from selenium.webdriver.common.by import By


class Property:
    def __init__(self, title, url, price):
        self.property_id = uuid.uuid4()
        self.title = title
        self.url = url
        self.price = int(price[1:])
    
def start_scraper(location, start_d, nights, guests, crawl_speed):
    try:
        start_chrome("https://www.booking.com", headless=False)
        click("Accept")
        write(location, into="Where are you going?")
        time.sleep(1 * crawl_speed)
        first_result = S('#autocomplete-result-0')
        click(first_result)

        time.sleep(1 * crawl_speed)
        date_elements = find_all(S('[data-date]'))
        if date_elements:
            for element in date_elements:
                date_value = element.web_element.get_attribute('data-date')
                if date_value == start_d:
                    click(element)
                    break
        date_elements = find_all(S('[data-date]'))
        if date_elements:
            end_d = datetime.strptime(start_d, '%Y-%m-%d') + timedelta(days=nights)
            for element in date_elements:
                date_value = element.web_element.get_attribute('data-date')
                if date_value == end_d.strftime('%Y-%m-%d'):
                    click(element)
                    break

        if guests == 1:
            occupancy_element = S('[data-testid="occupancy-config"]')
            click(occupancy_element)
            buttons = find_all(S('button[tabindex="-1"]'))
            if buttons:
                first_button = buttons[0]
                click(first_button)

        click("Search")
        time.sleep(3 * crawl_speed)
        dismiss_buttons = find_all(S('button[aria-label="Dismiss sign in information."]'))
        if dismiss_buttons:
            click(dismiss_buttons[0])
        time.sleep(2 * crawl_speed)
        click("Sort by:")
        click("Price (lowest first)")

        time.sleep(1 * crawl_speed)
        property_cards = find_all(S('[data-testid="property-card-container"]'))
        properties = []
        for card in property_cards:
            title_element = card.web_element.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]')
            title_text = title_element.text
            link_element = card.web_element.find_element(By.CSS_SELECTOR, 'a[data-testid="title-link"]')
            property_url = link_element.get_attribute('href')
            price_element = card.web_element.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]')
            price_text = price_element.text
            property = Property(title=title_text, url=property_url, price=price_text)
            properties.append(property)
            print(f"Property Found: {property.title} - £{property.price}")
        page_results = len(property_cards)
        print(f"Scraped {page_results} results from 1st page.")

        return properties

    except Exception as e:
        print(f"An error occurred: {e}")
        kill_browser()
        return False

def main():
    parser = argparse.ArgumentParser(description="Scrape Booking.com for hotel prices.")
    parser.add_argument("--location", type=str, default="Edinburgh", help="Location to search for hotels")
    parser.add_argument("--start_date", type=str, default=datetime.today().strftime('%Y-%m-%d'), help="Start date for booking in YYYY-MM-DD format")
    parser.add_argument("--nights", type=int, default=1, help="Number of nights to book (max 30)") # 30ish, technically however many nights are left until the end of the following month
    parser.add_argument("--guests", type=int, default=2, help="Number of guests (min 1 max 2)")
    parser.add_argument("--retries", type=int, default=5, help="Number of retries if scraping fails")
    parser.add_argument("--retry_delay", type=int, default=2, help="Delay between scraper retries in seconds")
    parser.add_argument("--crawl_speed", type=float, default=2.5, help="Speed multiplier for expected page loads (higher is slower)") # 1.0 is normal speed

    args = parser.parse_args()
    print(f"Searching for hotels in {args.location} from {args.start_date} for {args.nights} nights for {args.guests} guests...")

    for attempt in range(args.retries):
        print(f"Attempt {attempt + 1} of {args.retries}")
        properties = start_scraper(args.location, args.start_date, args.nights, args.guests, args.crawl_speed)
        if properties:
            print(f"Scraping completed in {attempt + 1} attempts. Found {len(properties)} properties.")

            total_price = 0
            cheapest_property = None
            for property in properties:
                total_price += property.price
                if cheapest_property is None or property.price < cheapest_property.price:
                    cheapest_property = property
            average_price = total_price / len(properties)

            print(f"Average price: £{average_price}")
            print(f"Cheapest property: {cheapest_property.title} - £{cheapest_property.price} - {cheapest_property.url}")
            break  # If scraping is successful, exit the retry loop
        else:
            print("Scraping failed, retrying...")
            time.sleep(args.retry_delay)
    else:
        print("Maximum retries reached. Scraping failed.")

if __name__ == "__main__":
    main()