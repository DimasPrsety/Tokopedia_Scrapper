# Cobain dari youtube
import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


# Declare url Tokopedia yang akan discrape
# url_baksoudang = 'https://www.tokopedia.com/search?st=&q=bakso%20udang&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #53 pages
# url_steakikan = 'https://www.tokopedia.com/search?st=&q=steak%20ikan&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #104 pages
# url_choppedvannamei = '' # Ga ada barangnya
url_fishball = 'https://www.tokopedia.com/search?st=&q=fish%20ball&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #201 pages
url_chikuwa = 'https://www.tokopedia.com/search?st=&q=chikuwa&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #56 pages
url_fishcake = 'https://www.tokopedia.com/search?st=&q=fish%20cake&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #276 pages
url_shrimpball = 'https://www.tokopedia.com/search?st=&q=shrimpi%20ball&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #42 pages
url_popcornikan = 'https://www.tokopedia.com/search?st=&q=popcorn%20ikan&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #3 pages
url_ebifurai = 'https://www.tokopedia.com/search?st=&q=ebi%20furai&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource=' #33 pages

url_tokopedia = [
    # url_baksoudang
    # , url_steakikan
    url_fishball
    , url_chikuwa
    , url_fishcake
    , url_shrimpball
    , url_popcornikan
    , url_ebifurai
]

# Preprocessing data and declaring variable
data = []
badge_mapping = {
    "https://images.tokopedia.net/img/official_store_badge.png": "official store"
    , "https://images.tokopedia.net/img/goldmerchant/pm_activation/badge/PM%20Pro%20Small.png": "gold merchant"
    , "https://images.tokopedia.net/img/power_merchant_badge.png": "power merchant"
}


driver = webdriver.Chrome()

for url in url_tokopedia : 
    print(f"Scraping URL : {url}")
    driver.get(url)
    page_counter  = 0

    while True : 
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#zeus-root")))
        time.sleep(2)
        
        for j in range (21): 
            driver.execute_script("window.scrollBy(0, 250)")
            time.sleep(1)

        current_url = driver.current_url

        driver.execute_script("window.scrollBy(50, 0)")
        time.sleep(1)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        products = soup.find_all('div', class_="css-5wh65g")

        # Extract product information
        for product in products:
            # Extract product name
            product_name_tag = product.find('span', class_='_0T8-iGxMpV6NEsYEhwkqEg==')
            product_name = product_name_tag.text.strip() if product_name_tag else 'N/A'

            # Extract price
            price_tag = product.find('div', class_='_67d6E1xDKIzw+i2D2L0tjw==')
            price = price_tag.text.strip() if price_tag else 'N/A'

            # Extract Location
            location_tag = product.find('span', class_='pC8DMVkBZGW7-egObcWMFQ== flip')
            location = location_tag.text.strip() if location_tag else 'N/A'        
            
            # Extract shop name
            shop_name_tag = product.find('span', class_='T0rpy-LEwYNQifsgB-3SQw== pC8DMVkBZGW7-egObcWMFQ== flip')
            shop_name = shop_name_tag.text.strip() if shop_name_tag else 'N/A'

            # Extract shop badge
            shop_badge_tag = product.find('img', class_='YtXczlnkXDXQ59u3vhDxiA==')
            shop_badge_src = shop_badge_tag['src'] if shop_badge_tag else None
            shop_badge = badge_mapping.get(shop_badge_src, "N/A")

            # Extract rating
            rating_tag = product.find('span', class_='_9jWGz3C-GX7Myq-32zWG9w==')
            rating = rating_tag.text.strip() if rating_tag else 'N/A'

            # Extract number of items sold
            sold_tag = product.find('span', class_='se8WAnkjbVXZNA8mT+Veuw==')
            sold = sold_tag.text.strip() if sold_tag else 'N/A'

            scrape_time = datetime.now().strftime("%Y-%m-%d $H:%M:%S")

            # Store the data in a set to avoid duplicates
            data.append(
                (product_name, price, location, shop_name, shop_badge, rating, sold, current_url, scrape_time)
            )
        
        page_counter += 1
        print(f"Scraped page {page_counter} of URL : {url}")
        time.sleep(2)

        # Check if "Laman Berikutnya" disabled 
        try : 
            next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Laman berikutnya']")
            if next_button.get_attribute("disabled") : 
                print("Last page reached. Exiting Loop")
                break
            next_button.click()
            time.sleep(4)
        except Exception as e : 
            print("Next button not found. Scrolling back up.")
            for k in range(2) : 
                driver.execute_script("window.scrollBy(0, -250)")
                time.sleep(1)
            try : 
                #Retrying to find and click the "Next" Button
                next_button.click()
                time.sleep(4)
            except Exception as e : 
                print("Next button still not found after scrolling up")
                break # Exit the loop for the current URL
                
df = pd.DataFrame(data, columns = ['Product_name', 'price', 'location', 'shop_name', 'shop_badge', 'rating', 'sold', 'Source_url', 'Scrape_time'])

driver.quit()

df = pd.DataFrame(data, columns = ['Product_name', 'price', 'location', 'shop_name', 'shop_badge', 'rating', 'sold', 'Source_url', 'Scrape_time'])
# df.to_excel('tokopedia_all_products3.xlsx')
df.to_parquet("data.parquet", engine="pyarrow") 
print("File parquet telah dibuat.")