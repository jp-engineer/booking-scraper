# Booking Scraper

This Booking.com Scraper is a Python-based tool designed to scrape hotel, hostel, and apartment prices from the Online Travel Agent (OTA) "booking.com" for a specified location. More specifically it finds the cheapest accommodation options and calculates the average price for a given date range. It leverages the Helium library, which provides a high-level API for web scraping using Selenium.

## Features

- Location-Based Search: Specify any location to search for available accommodations.
- Flexible Date Range: Define the start date and number of nights to book.
- Occupancy Settings: Supports different guest counts, accommodating up to two guests.
- Price Analysis: Calculates the average price of available accommodations and identifies the cheapest option.
- Command-Line Interface (CLI): Easily customizable via CLI arguments.
- Error Handling & Retry Mechanism: Includes a robust retry mechanism to handle occasional scraping failures.

## Limitations

At present:

    - there is no support for headless browsing
    - the max number of occupants is 2, sharing 1 room, apartment or 2 dormitory beds

## Setup

1. Clone the repository:

    ```shell
    git clone https://github.com/jp-engineer/booking-scraper.git
    ```

2. Create a virtual environment:

    ```shell
    python -m venv env
    ```

3. Activate the virtual environment:

    ```shell
    source env/bin/activate
    ```

4. Install the required packages:

    ```shell
    pip install -r requirements.txt
    ```

## Command-Line Arguments
--location (str, default="Edinburgh"): Specifies the location where you want to search for accommodations.

--start_date (str, default=today's date in "YYYY-MM-DD" format): The start date for booking in YYYY-MM-DD format.

--nights (int, default=1): Number of nights to book. The maximum allowed value is 30.

--guests (int, default=2): Number of guests. Supports a minimum of 1 and a maximum of 2 guests.

--retries (int, default=5): Number of retries if scraping fails due to issues like loading errors or network interruptions.

--retry_delay (int, default=2): Delay (in seconds) between retry attempts if scraping fails.

--crawl_speed (float, default=2.5): Speed multiplier for page loading. A higher value slows down the scraping process, which can be useful for dealing with slower page loads.

## Example-Usage

To run the scraper, use the following command:

```shell
python scraper.py --location "London" --start_date "2024-09-15" --nights 2 --guests 1 --retries 3 --crawl_speed 1.0

```

## Disclaimer: 
This scraper is intended for educational purposes only. The use of automated scraping on Booking.com or any other website may violate their terms of service and could result in your IP being banned. The author takes no responsibility for any consequences arising from the use of this tool.

## Contribution 
If you would like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request. Contributions, whether in the form of bug fixes, new features, or documentation improvements, are always welcome.

## dev notes:
This scraper was created as an educational project to explore the capabilities of the Helium library for Python in a quick, 2-hour "hackathon" style session. While it is functional, it is important to note that this is not a production-grade tool and comes with several limitations. It's designed to be straightforward, lacking advanced features such as proxy IPs, spoofed user agents, or sophisticated interaction patterns and this means it doesn't employ techniques to avoid detection, and i'ts use could potentially lead to being blocked or banned by Booking.com. That being said, the default settings of the scraper are intentionally conservative and are designed to minimize load on Booking.com's servers.

The main goals for the project were:

    - Calculate the average price of accommodations in a specified location over the next 30 days.
    
    - Identify the cheapest accommodation, including its price and URL.
    
    - Support various combinations of nights and occupancy levels.
        
    - Implement a full-featured command-line interface (CLI).
    
    - Use only the Helium library for web scraping.
    
    - Keep the script concise, aiming for roughly 100 lines of code.

Outcomes:
    
    - Success: Achieved goals (a), (b), (c), and (d), providing a functional scraper with robust CLI support.
    
    - Partial Success: The project slightly exceeded the 100-line goal and incorporated additional libraries (such as the underlying Selenium framework) to handle edge cases and improve reliability.

    - Failures: Never could get full headless support working in the alloted time.
