from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

class Oklahoma_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        url = "https://www.sos.ok.gov/corp/corpinquiryfind.aspx"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)
        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_xpath('//*[@id="ctl00_DefaultContent_CorpNameSearch1__singlename"]')
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="ctl00_DefaultContent_CorpNameSearch1_SearchButton"]')
        submit.click()
        # finds and navigates to the link for the first entity
        # times out after 15 seconds of the results loading
        try:
            WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="ctl00_DefaultContent_CorpNameSearch1_EntityGridView"]/div/table/tbody/tr[1]/td[1]/a')))
        except Exception:
            print("Timed Out After 15 Seconds")
            print("Please Try Again")
            driver.quit()
            sys.exit()
        link = driver.find_element_by_xpath(
            '//*[@id="ctl00_DefaultContent_CorpNameSearch1_EntityGridView"]/div/table/tbody/tr[1]/td[1]/a')
        link.click()
        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # creates dictionary
        fullDict = {}
        headers = driver.find_elements_by_class_name('SummaryBoxHeader')
        boxes = driver.find_elements_by_class_name('ftable')
        for i in range(len(boxes)):
            fullDict[headers[i].text] = {}
            keys = boxes[i].find_elements_by_tag_name('dt')
            values = boxes[i].find_elements_by_tag_name('dd')
            for j in range(len(keys)):
                fullDict[headers[i].text][keys[j].text] = values[j].text
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)
        return self.scrapeData(driver)
