import json

import undetected_chromedriver as  webdriver
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import string
import random
import time
import requests
import pandas as pd
from flask import Flask, request, jsonify
import threading
import queue

app = Flask(__name__)

# Queue to handle requests
request_queue = queue.Queue()
def scraper_function(link, result_queue):
    try:

        options = webdriver.ChromeOptions()
        # options.add_argument(r'--profile-directory=C:\\Users\\Ahmad\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3')
        options.add_argument("--disable-renderer-backgrounding")
        options.add_argument("--disable-backgrounding-occluded-windows")
        #options.add_argument("--headless")
        windows_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        scraped_data={}



        options.add_argument(f"--user-agent={windows_user_agent}")
        options.add_argument("--window-size=1920x1080")

        options.add_argument('--load-extension=SimplyTrends')
        browser = webdriver.Chrome(options=options)

        i = random.randint(2, 57)
        cookies_file = 'cookies_simpletrends.json'
        try:

            browser.get('https://app.simplytrends.co/salestracking/start')

            # cookies = browser.get_cookies()
            # print("Cookies from first site:", cookies)
            # with open(cookies_file, 'w') as file:
            #   json.dump(cookies, file)
            # print("Cookies saved to file.")
            # browser.delete_all_cookies()
            #
            #  # Apply each cookie
            # for cookie in cookies:
            #      browser.add_cookie(cookie)

            with open(cookies_file, 'r') as file:
                cookies = json.load(file)

            # Clear existing cookies in the browser
            browser.delete_all_cookies()

            # Add new cookies
            for cookie in cookies:
                browser.add_cookie(cookie)
            # Open the second website
            print('done')

            # Refresh the page to apply cookies
            browser.refresh()
            # browser.get('https://app.simplytrends.co/shopifystore/barnerbrand.com')
            browser.get(link)
            domain = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#appBarContainer > div > div > p > p > a.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineHover.css-1xa0emq > p')))
            domain_name = domain.text
            dot_position = domain_name.find('.')

            # Extract the text from the dot position to the end of the string
            extension = domain_name[dot_position:] if dot_position != -1 else ''

            print(extension)
            scraped_data['domain_name'] = domain.text
            monthlyunites = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div/div/div/p')))
            monthlyunites = monthlyunites.text
            print(monthlyunites)
            scraped_data['monthlyunites'] = monthlyunites

            monthlyrevenue = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div/div/div/p')))
            monthlyrevenue = monthlyrevenue.text
            print(monthlyrevenue)
            scraped_data['monthlyrevenue'] = monthlyrevenue
            country = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(3) > div > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-item.MuiGrid-grid-xs-12.css-ta72l6 > div:nth-child(1) > div > div > div > div > p > div > span')))
            country = country.text
            print(country)
            scraped_data['country'] = country
            try:
                countryrank = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[2]/div/div/div/div/div[3]/div/div/div[1]/div[4]/div/div/div/div/p')))
                countryrank = countryrank.text
            except:
                countryrank = "-"
            print(countryrank)
            scraped_data['countryrank'] = countryrank
            try:
                socialmedia = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(3) > div > div > div.css-1t62lt9 > span > a')))
                href = socialmedia.get_attribute('href')
            except:
                href = "-"
            print("Extracted URL:", href)
            scraped_data['socialmedia'] = href
            monthstats = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(4) > div > h2 > span > p > div')))
            monthstats = monthstats.text
            print(monthstats)
            scraped_data['monthstats'] = monthstats
            language = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(3) > div > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-item.MuiGrid-grid-xs-12.css-ta72l6 > div:nth-child(2) > div > div > div > div > p')))
            language = language.text
            print(language)
            scraped_data['language'] = language
            currency = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(3) > div > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-item.MuiGrid-grid-xs-12.css-ta72l6 > div:nth-child(3) > div > div > div > div > p')))
            currency = currency.text
            print(currency)
            scraped_data['currency'] = currency
            firstpublishproduct = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(4) > div > div:nth-child(3) > div:nth-child(1) > div > div > div > div > p')))
            firstpublishproduct = firstpublishproduct.text
            print(firstpublishproduct)
            scraped_data['firstpublishproduct'] = firstpublishproduct
            lastpublishproduct = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(4) > div > div:nth-child(3) > div:nth-child(2) > div > div > div > div > p')))
            lastpublishproduct = lastpublishproduct.text
            print(lastpublishproduct)
            scraped_data['lastpublishproduct'] = lastpublishproduct
            numproducts = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(4) > div > div:nth-child(3) > div:nth-child(3) > div > div > div > div > p')))
            numproducts = numproducts.text
            print(numproducts)
            scraped_data['numproducts'] = numproducts
            avgprices = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(4) > div > div:nth-child(3) > div:nth-child(4) > div > div > div > div > p > span')))
            avgprices = avgprices.text
            print(avgprices)
            scraped_data['avgprices'] = avgprices
            highestproductprice = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(4) > div > div:nth-child(3) > div:nth-child(5) > div > div > div > div > p > a > span')))
            highestproductprice = highestproductprice.text
            print(highestproductprice)
            scraped_data['highestproductprice'] = highestproductprice
            lowestproductprice = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                '#__next > div > div.app-container-box.MuiBox-root.css-w8kjuh > div > div > div > div > div:nth-child(4) > div > div:nth-child(3) > div:nth-child(6) > div > div > div > div > p > a > span')))
            lowestproductprice = lowestproductprice.text
            print(lowestproductprice)
            scraped_data['lowestproductprice'] = lowestproductprice
            try:
                ch = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[2]/div/div/div/div/div[4]/div/div[2]/div[3]/div/div/div/div/div[8]/p'))).click()
                ch = WebDriverWait(browser, 120).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[3]/div[3]/div/div')))
            except:
                ch = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[1]/div/div[2]/div/div/div/div/div[4]/div/div[2]/div[3]')))
                pass
            time.sleep(1)

            div_html = ch.get_attribute('innerHTML')

            soup = BeautifulSoup(div_html, 'html.parser')

            # Define a list to hold all the rows of data
            data = []

            vendor_divs = soup.find_all('div', class_='css-69i1ev')

            # Loop through the vendor divs to extract the data
            for vendor in vendor_divs:
                # Extract the vendor name

                # time.sleep(30)
                # vendor_name = vendor.find('a').get_text(strip=True)
                # distribution_span = vendor.find('span')
                distribution_span = vendor.find('a', class_='css-1xa0emq')
                vender_span = vendor.find('div', class_='css-1vtkzp1')
                vendor_name = vender_span.find('span').get_text(strip=True) if distribution_span else 'Unknown'

                # Extract the distribution percentage
                # distribution_span = vendor.parent.find('span', class_='css-15nru74')
                spans = vendor.parent.find_all('span', class_='css-15nru74')

                # Select the span you want by index, e.g., the second span
                if len(spans) > 1:
                    desired_span = spans[1]  # This is the second span
                    # Now you can extract the text or any other attribute from the desired_span
                    distribution = desired_span.get_text(strip=True)
                else:
                    distribution = 'N/A'
                # distribution_span = distribution_span.find_next_sibling('span', class_='css-15nru74')
                # distribution = distribution_span.get_text(strip=True) if distribution_span else 'Unknown'

                # Extract the number of products. It's in the next div with class 'css-18jpfvm'
                # num_products = vendor.find_next_sibling('div', class_='css-18jpfvm').get_text(strip=True)
                # num_products = vendor.find_next_sibling('div', class_='css-18jpfvm').find('p').get_text(strip=True)
                num_products_div = vendor.parent.find_next_sibling('div', class_='css-18jpfvm')
                num_products = num_products_div.find('p').get_text(
                    strip=True) if num_products_div else 'Unknown'

                # Append the data to the list
                data.append({'Vendor': vendor_name, 'Distribution': distribution,
                             'Number of products': num_products})

            # Create a DataFrame

            df = pd.DataFrame(data)

            # Print the DataFrame
            print(df)
            scraped_data['Vendor_table'] = data
            try:
                click = WebDriverWait(browser, 2).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '/html/body/div[3]/div[3]/div/div/button'))).click()
            except:
                pass

            click = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/div[1]/div/div[2]/div/div/div/div/div[4]/div/div[2]/div[6]/div/div/div/div/div/div[8]/p'))).click()
            time.sleep(1)
            click = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/div[3]/div[3]/div/div')))

            div_html = click.get_attribute('innerHTML')

            soup = BeautifulSoup(div_html, 'html.parser')

            # Define a list to hold all the rows of data
            data_producttags = []

            vendor_divs = soup.find_all('div', class_='css-69i1ev')

            # Loop through the vendor divs to extract the data
            for vendor in vendor_divs:
                # Extract the vendor name
                vendor_name = vendor.find('a').get_text(strip=True)

                # Extract the distribution percentage
                distribution_span = vendor.find('a').find_next_sibling('span')
                distribution = distribution_span.get_text(strip=True) if distribution_span else 'Unknown'

                # Extract the number of products. It's in the next div with class 'css-18jpfvm'
                # num_products = vendor.find_next_sibling('div', class_='css-18jpfvm').get_text(strip=True)
                # num_products = vendor.find_next_sibling('div', class_='css-18jpfvm').find('p').get_text(strip=True)
                num_products_div = vendor.parent.find_next_sibling('div', class_='css-18jpfvm')
                num_products = num_products_div.find('p').get_text(
                    strip=True) if num_products_div else 'Unknown'

                # Append the data to the list
                data_producttags.append({'Product_tag': vendor_name, 'Distribution': distribution,
                                         'Number of products': num_products})

            # Create a DataFrame

            df_producttags = pd.DataFrame(data_producttags)

            # Print the DataFrame
            print(df_producttags)
            scraped_data['df_producttags'] = data_producttags
            click = WebDriverWait(browser, 120).until(
                EC.presence_of_element_located((By.XPATH,
                                                '/html/body/div[3]/div[3]/div/div/button'))).click()

            browser.quit()


        except  Exception as e:

            pass





    except:


        browser.quit()
        print('exception')

    result_queue.put(scraped_data)
def convertTuple(tup):

    strc = ''
    c = len(tup)

    for item in range(5):
        strc = strc + strc.join(tup[item])

    return strc


letters = string.ascii_lowercase




mobile_emulation = {"deviceName": "iPhone SE"}
# options.add_experimental_option("mobileEmulation", mobile_emulation)
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
# options.add_experimental_option("mobileEmulation", mobile_emulation)
count = 0
recount = 100
total = 0

from bs4 import BeautifulSoup
def find_first_link(text):
    # Regular expression pattern for finding URLs
    pattern = r'https?://\S+'
    match = re.search(pattern, text)
    return match.group(0) if match else None
def generate_random_username(length=10):
    all_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    username = ''.join(random.choice(all_characters) for _ in range(length))
    return username
greetings = ["Hello", "Hi", "Hey", "Greetings", "Howdy"]
subjects = ["this article", "your post", "the blog", "the content", "this page"]
verbs = ["is amazing", "is interesting", "was enlightening", "is insightful", "is impressive"]
adverbs = ["really", "truly", "absolutely", "definitely", "certainly"]
compliments = ["great job", "excellent work", "fantastic read", "good stuff", "wonderful insight"]

def generate_comment():
    # Randomly pick parts of the sentence
    greeting = random.choice(greetings)
    subject = random.choice(subjects)
    verb = random.choice(verbs)
    adverb = random.choice(adverbs)
    compliment = random.choice(compliments)

    # Construct the comment
    comment = f"{greeting}, {subject} {verb}. {adverb} {compliment}!"
    return comment

def is_liked(soup_svg):
    return bool(soup_svg.find('clipPath', {'id': '__lottie_element_8932'}))


import threading
# Other imports remain the same

# Define the function that each thread will execute
def thread_function(cookies_file, file_path_follow, file_path_like, file_path_comment):
    try:
        options = webdriver.ChromeOptions()
        # ... (other options setup)

        browser = webdriver.Chrome(options=options)

        # Load cookies from the specified file
        with open(cookies_file, 'r') as file:
            cookies = json.load(file)
            for cookie in cookies:
                browser.add_cookie(cookie)
        browser.refresh()

        # Your existing logic for follow, like, and comment
        # ...
        # Make sure to use the file_path_follow, file_path_like, and file_path_comment variables
        # ...

        browser.quit()

    except Exception as e:
        print(str(e))
        browser.quit()

# Main execution


@app.route('/scrape', methods=['POST'])
def scrape():
    link = request.json.get('link')
    result_queue = queue.Queue()

    # Start a new thread for each scraping request
    thread = threading.Thread(target=scraper_function, args=(link, result_queue))
    thread.start()

    # Wait for the result
    result = result_queue.get()

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)






















