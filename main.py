from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import requests

load_dotenv()

bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']


url ="https://whatson.bfi.org.uk/imax/Online/default.asp?BOparam::WScontent::loadArticle::permalink=interstellar"

message_text = f'IMAX show for BFI Intestellar is open! Grab your seat! {url}'

if not bot_token or not chat_id:
    print("You are missing your BOT_TOKEN and/or CHAT_ID")
    exit(1)

def check():
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

    # Wait 5 secs to let Cloudflare pass
  time.sleep(5)

  if 'No-Showtimes-First' in driver.page_source:
        print("No showtimes available")
        driver.quit()
        return
  else:
        print("Showtimes are available!")


 # Send message to Telegram bot
  telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
  params = {'chat_id': chat_id, 'text': message_text}
  response = requests.post(telegram_api_url, data=params)
  print(response)

    # Prevent sending the message again
  with open(sent_flag_file, 'w') as f:
        f.write("1")
  print("Notification sent!")

  driver.quit()


check()

#   cookies = {
#       'connect.sid': 's%3AMHDc0Bw69sYY2ygTnQtxJDBXF7A-bMnl.PLQoESGqCf9GmTA3o6ZRfIj9dqbxCnXjInBhyHwyFEo',
#       'TS016dea95':  '01a483b971e5a615771b97d9ce06132a6563db5f4da50eb61483c00f7c316193a93ff162ef5423e80bfc62cd37e8cc28dd90a3375e',
#       'TS01c7b029': '01a483b971e5a615771b97d9ce06132a6563db5f4da50eb61483c00f7c316193a93ff162ef5423e80bfc62cd37e8cc28dd90a3375e',
#       '__cf_bm':    'RS2i0B4SiZO8BzOa3j4b.e2QaYQhgsEAa2_J0iW4.Lk-1709733853-1.0.1.1-jSOsqOXfBxRM0d_ZgdW_FUi0lrmT7BGwB5TUrIio5RoFz2yCDomfyfJN2EVVMbApq_EFohVuQaTMiz2dGBPGrA',
#       'osano_consentmanager_uuid': 'bd0321ed-48ce-4db9-984f-6281f3106f0e',
#       'osano_consentmanager': 'rvUIHzBxgOW6jhX4w11_PBkJ65PbGteMIu8sVjD0kK_scI52kX2LHtdKJecU33pi-IH8SjWb__JlIEWcbDqcw8gzC0rrPDpoZhZ94PUnHlhBAdhK75NK9UwNkg_M7c3NhbzOmpv6Bw5rkczfOt8wHharGkivtRAp6TbfWd9v6-jhnZbM5pzZFVvGVYIaO3kPpMWI3C9lIVctyn-DMhMf-5tC_Too8X4Ab33aJkjqHlAVfZN7DjvIrTHPQZhb0BsKyHiPZ0q4UPRKjY5bjmhjUUDFVlz6_HQ54Q8lOQ==',
#       'cf_clearance': '_g6wT9GlUhCXlLycUz_ZFPGEWySzLrXX0sKNHadTiEM-1709733854-1.0.1.1-5tFPrDqDa3s.8c6kga7n394vaVOhfLCe5dFw8_XQHEJHIl3UP4leE5xPDdV3lkfBA0FTIYPrSWNz5KLw4.1MSA',
#       '_gcl_au': '1.1.698670245.1709733855',
#       '_tt_enable_cookie': '1',
#       '_ttp': 'DWkyjs2kADpfN25Mlg5T2GPW6yv',
#       '_fbp': 'fb.1.1709733854966.252695757',
#       '_gid': 'GA1.2.863061711.1709733855',
#       '_dc_gtm_UA-24750557-1': '1',
#       '_scid': '98b356ca-41d0-47aa-adca-534768a5f93b',
#       '__adroll_fpc': '3de2b3a216370c682799c63606500bb1-1709733855192',
#       '_sctr': '1%7C1709701200000',
#       'alreadyLanded': 'true',
#       '_gat_UA-24750557-1': '1',
#       'TS01e39824': '01a483b971fb7a29dcba33dd1d6b916275c62b17144cf241f7e39d88b03808391007bc6d047b08ffb2fac63e04e822fb21aa9e6ae2',
#       '_uetsid': '6a4dbaa0dbc211eead72c90ea61eedde',
#       '_uetvid': '6a4df6f0dbc211ee97c36f0d3bc53e1c',
#       '_ga': 'GA1.2.801642614.1709733855',
#       '_scid_r': '98b356ca-41d0-47aa-adca-534768a5f93b',
#       '__ar_v4': 'CV77WC2OENGF5J3JPC3ZXW%3A20240305%3A3%7CRUHEGRL6TVGN3OZ3D24MKD%3A20240305%3A3%7C6JBCD3ZQSBDZ5B73FXG2OG%3A20240305%3A3',
#       'pageCookie_1': url.replace("https://whatson.bfi.org.uk", ""),
#       '_ga_3FBVCHD93B': 'GS1.1.1709733854.1.1.1709733898.16.0.0',
#   }

#   headers = {
#       'authority': 'www.whatson.bfi.org.uk',
#       'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#       'accept-language': 'en-GB,en;q=0.9',
#       'cache-control': 'max-age=0',
#       'dnt': '1',
#       'sec-ch-ua': '"Google Chrome";v="122", "Chromium";v="122", "Not:A-Brand";v="99"',
#       'sec-ch-ua-mobile': '?0',
#       'sec-ch-ua-platform': '"Windows"',
#       'sec-fetch-dest': 'document',
#       'sec-fetch-mode': 'navigate',
#       'sec-fetch-site': 'same-origin',
#       'sec-fetch-user': '?1',
#       'upgrade-insecure-requests': '1',
#       'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#   }

