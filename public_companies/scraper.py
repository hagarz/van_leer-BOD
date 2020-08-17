__author__ = 'Hagar Zemach'

from selenium import webdriver
from selenium import common
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os

PATH = r'<chromedriver_path>'


class SeleniumManager(object):
    """Retrieves data from Tel Aviv Stock Exchange """
    def __init__(self):
        self.options = Options()
        self.options.page_load_strategy = 'none'
       # self.options.add_argument('--disable-gpu')
        self.base_url = "http://maya.tase.co.il"

    def get_company_details(self, company_id):
        url = self.base_url+f'/bursa/CompanyDetails.asp?CompanyCd={company_id}'

    def get_all_reports(self, from_year, to_year):
        url = self.base_url + f'/reports/finance?q=%7B%22Period%22:%224%22,%22FromYear%22:{from_year},' \
                                            f'%22ToYear%22:{to_year}%7D'

    def get_company_reports(self, company_id, from_year, to_year):
        """ Returns url to pdf file of 2019 annual report of company for download"""
        self.options = Options()
        self.options.page_load_strategy = 'none'
        self.driver = webdriver.Chrome(PATH)
        self.driver.set_page_load_timeout(60)

        # service = Service(PATH)
        # service.start()
        # self.driver = webdriver.Remote(service.service_url, options=self.options)
        url = self.base_url + f'/reports/finance?q=%7B%22Period%22:%224%22,%22FromYear%22:{from_year},' \
                                              f'%22ToYear%22:{to_year},%22EntityId%22:{company_id}%7D'
        flag = True
        n = 0
        while flag:
            try:
                self.driver.get(url)
                time.sleep(2 + n)  # Let the user actually see something!
                reports_page = self.driver.find_element_by_xpath('//div[@class="listTable"]//*'
                                                                 '[contains(@href, "/2/0")]')
                flag = False
            except (common.exceptions.NoSuchElementException, common.exceptions.TimeoutException):
                if n == 5:
                    self.driver.quit()
                    return None
                n += 1
                pass
        report_link = reports_page.get_attribute("href")
        n = 0
        flag = True
        while flag:
            try:
                self.driver.get(report_link)
                time.sleep(5 + n)
                pdf_page_element = self.driver.find_element_by_xpath('//div[@class="feedItemButton"]//*[@file]')
                flag = False
                if pdf_page_element.get_attribute('file') == "":
                    if n < 5:
                        n += 1
                        flag = True
                    else:
                        self.driver.quit()
                        return None
            except (common.exceptions.NoSuchElementException, common.exceptions.TimeoutException):
                pass
        pdf_page = pdf_page_element.get_attribute('file')
        self.driver.quit()
        return pdf_page

    def quit(self):
        self.driver.quit()
