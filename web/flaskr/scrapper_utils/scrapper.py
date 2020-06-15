import re
import sys

import redis
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class ScrapperService:

    def __init__(self):
        time.sleep(6)
        self.chrome = webdriver.Remote(
            command_executor='http://chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME)
        self.db = redis.Redis(host='redis', port=6379)


    def fill_urls_list(self, page_counter=1):

        page_index = 1

        while page_index < 500:
            try:
                self.chrome.get(
                    f"https://www.olx.pl/dom-ogrod/?view=galleryWide&page={page_index}&search[filter_enum_state][0]=new")
                WebDriverWait(self.chrome, 10).until(ec.visibility_of_element_located((By.XPATH, '//ul[@id="gallerywide"]')))
                products = self.chrome.find_elements_by_xpath('//ul[@id="gallerywide"]/li/div[@class="mheight tcenter"]/a')
                urls = [(re.search('oferta/(.*).html#', url.get_attribute('href')).group(1)) for url in products]

                self.db.lpush('links', *urls)

                page_index = page_index + 1
            except WebDriverException as e:
                print("Exception occured: ", e.__str__(), flush=True)
                self.chrome.quit()
                self.__init__()


        return self.chrome.title


