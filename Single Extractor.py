from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import requests
import time
from bs4 import BeautifulSoup
import json
import pandas as pd

# Automatically download and install the correct chromedriver version
chromedriver_autoinstaller.install()

# Read URLs from the CSV file
df = pd.read_csv('C:\\Users\\HP\\OneDrive\\Documents\\Thesis\\Code\\Top 2k.csv')
urls = df['URL'].tolist()  # Assuming the column is named 'URL'

# Set up the Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=chrome_options)

for url in urls:
    try:
        # Initialize the WebDriver and open the page
        driver.get('https://' + url)
        time.sleep(2)

        # Retrieve the User-Agent from the browser
        user_agent = driver.execute_script("return navigator.userAgent;")

        # Use the retrieved User-Agent in the headers for requests
        headers = {"User-Agent": user_agent}

        # Make the request using the requests library with the custom headers
        response = requests.get('https://' + url, headers=headers)

        # Parse the HTML content to extract JavaScript code
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script')
        javascript_code = [tag.string for tag in script_tags if tag.string]

        # Prepare the data to save in JSON format
        data = {
            "User-Agent": user_agent,
            "JavaScript": javascript_code
        }

        # Save the data to a JSON file
        file_path = f'C:\\Users\\HP\\OneDrive\\Documents\\Thesis\\Code\\JavaScripts\\{url}.json'
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"JavaScript code saved to {file_path}")

    except Exception as e:
        print(f"Failed to process {url}: {str(e)}")

# Close the WebDriver after processing all sites
driver.quit()
