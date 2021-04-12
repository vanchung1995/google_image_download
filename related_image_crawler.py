import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from multiprocessing import Process, Value, Array
from multiprocessing import Pool
import time

class RelatedImageCrawler:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.delay = 3 # seconds

    def worker(self,link):
        link.click()
        time.sleep(2)
        result_container = self.driver.find_element_by_id("islsp")
        all_result_links = result_container.find_elements_by_tag_name('img')
        for l in all_result_links:
            src = l.get_attribute('src')
            if not src.startswith('data:image') and "https://encrypted-tbn0.gstatic.com/" not in src:
                return src

    def crawl(self, related_url, max = 30):
        # def worker(link):
        #     link.click()
        #     time.sleep(2)
        #     result_container = self.driver.find_element_by_id("islsp")
        #     all_result_links = result_container.find_elements_by_tag_name('img')
        #     for l in all_result_links:
        #         src = l.get_attribute('src')
        #         if not src.startswith('data:image') and "https://encrypted-tbn0.gstatic.com/" not in src:
        #             print(src)
        #             return src
        origin_urls = []
        self.driver.get(related_url)
        container_elem = self.driver.find_element_by_id("islrg")
        all_links = container_elem.find_elements_by_tag_name('a')
        count = 0
        with Pool() as pool:
            for b in all_links[:]:
                href = b.get_attribute('href')
                if href is None:
                    if count == max:
                        return origin_urls
                    count += 1
                    b.click()
                    time.sleep(2)
                    result_container = self.driver.find_element_by_id("islsp")
                    all_result_links = result_container.find_elements_by_tag_name('img')
                    for l in all_result_links:
                        src = l.get_attribute('src')
                        if not src.startswith('data:image') and "https://encrypted-tbn0.gstatic.com/" not in src:
                            origin_urls.append(src)
        return origin_urls
