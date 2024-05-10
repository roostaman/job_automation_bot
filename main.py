from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
from time import sleep

FORM_URL = "https://forms.gle/BEEYk8M7LoCS4XxM7"
ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"


# get rent variants from zillow website and make a listing of their address, price, link
# used bs4 for scraping zillow website
class GetZillowContent:
    def __init__(self):
        response = requests.get(url=ZILLOW_URL)
        self.zillow_content = response.text
        try:
            self.soup = BeautifulSoup(self.zillow_content, "html.parser")
            self.listings_content = self.soup.find_all("li", class_="ListItem-c11n-8-84-3-StyledListCardWrapper")
        except Exception as ex:
            print(ex)
            pass
        self.links_list = []
        self.addresses_list = []
        self.prices_list = []
        self.length = 0

    def get_listings(self):
        try:
            self.links_list = [(listing.select_one("a[data-test='property-card-link']")).get("href") for listing in
                               self.listings_content]

            self.addresses_list = [(listing.select_one("address[data-test='property-card-addr']")).get_text(strip=True)
                                   for
                                   listing in self.listings_content]

            self.prices_list = [((listing.select_one("span[data-test='property-card-price']")).get_text(strip=True))[:6]
                                for
                                listing in self.listings_content]
            self.length = len(self.links_list)
        except Exception as ex:
            print(ex)
            pass


# fill to google form and sheet, parsed info from zillow class
# used selenium to fill the form
class FillForm:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def fill_field(self):
        self.driver.get(url=FORM_URL)
        sleep(3)

        for i in range(zillow.length):
            try:
                form_fields = self.driver.find_elements(By.CSS_SELECTOR, value="input[type='text']")
                # print(f"form_len: {len(form_fields)}\n")
                print(i, "/", zillow.length)
                sleep(3)
                form_fields[0].send_keys(zillow.addresses_list[i])
                # print(zillow.addresses_list[i])
                form_fields[1].send_keys(zillow.prices_list[i])
                form_fields[2].send_keys(zillow.links_list[i])
                sleep(2)

                send_button = self.driver.find_element(By.CSS_SELECTOR, value="div[role='button'].uArJ5e.UQuaGc.Y5sE8d")
                send_button.click()
                sleep(3)

                self.driver.get(url=FORM_URL)
                sleep(3)
            except Exception as ex:
                print(ex)
                pass


zillow = GetZillowContent()
zillow.get_listings()
# print(zillow.links_list)

fill_form = FillForm()
fill_form.fill_field()
