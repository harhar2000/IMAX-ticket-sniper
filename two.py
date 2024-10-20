from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
import requests

load_dotenv()

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']

url = "https://whatson.bfi.org.uk/imax/Online/default.asp?BOparam::WScontent::loadArticle::permalink=interstellar"

message_text = f'IMAX show for BFI Interstellar is open for your selected date! Grab your seat! {url}'

if not bot_token or not chat_id:
    print("You are missing your BOT_TOKEN and/or CHAT_ID")
    exit(1)

def check_for_date(show_date):
    sent_flag_file = 'sent_flag.txt'
    if os.path.exists(sent_flag_file):
        with open(sent_flag_file, 'r') as f:
            if f.read().strip() == "1":
                print("Already notified. Stop the Repl deployment when you can.")
                return

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Initialise Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    try:
        # Wait for the showtimes section to load (you may need to adjust the element)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'showtimes')]"))  # Adjust this based on your findings
        )

        # Fetch the section that contains the dates and showtimes
        showtime_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'showtimes')]//time")  # Adjust XPath based on actual HTML

        # Iterate over the found elements and check for the specific date
        for element in showtime_elements:
            showtime_text = element.text.strip()
            if show_date in showtime_text:
                print(f"Showtimes are available for {show_date}!")

                # Send message to Telegram bot
                telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                params = {'chat_id': chat_id, 'text': message_text}
                response = requests.post(telegram_api_url, data=params)
                print(response)

                # Prevent sending the message again
                with open(sent_flag_file, 'w') as f:
                    f.write("1")
                print("Notification sent!")
                break
        else:
            print(f"No showtimes available for {show_date}.")
        
    except Exception as e:
        print("Error loading showtimes:", e)
    
    finally:
        driver.quit()

# Get the user input for the desired date
user_input_date = input("Enter the date to check for (e.g., Monday 21 October): ")

# Format the input date to match the format in the HTML (if needed)
formatted_date = user_input_date.strip()  # Ensure there are no leading or trailing spaces

check_for_date(formatted_date)
