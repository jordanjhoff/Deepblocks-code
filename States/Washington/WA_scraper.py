from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Washington_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        url = "https://ccfs.sos.wa.gov/#/AdvancedSearch"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver
    
    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        time.sleep(2)
        text = driver.find_element_by_id("txtOrgname")
        text.send_keys(entity_name)
        wait = WebDriverWait(driver, 30)
        submit = wait.until(EC.element_to_be_clickable((By.ID, 'btnSearch')))
        driver.implicitly_wait(8000)
        submit.click()
        driver.implicitly_wait(8000)
        link = driver.find_element_by_xpath(
            '/html/body/div[1]/ng-include/div/section/div[2]/div[1]/div/div[2]/div/div[1]/table/tbody[1]/tr/td[1]/a')
        driver.implicitly_wait(8000)
        link.click()

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # scrapes information and officers
        fullDict = {
            'Information': {},
            'Registered Agent': {},
            'Officers': {}
        }
        time.sleep(5)
        test = driver.find_element_by_id('divmain')
        info = test.find_elements_by_class_name('col-md-3')
        for i in range(0, len(info), 2):
            if i + 1 < len(info):
                fullDict['Information'][info[i].text] = info[i + 1].text
            else:
                fullDict['Information'][info[i].text] = ""
        agents = test.find_elements_by_class_name('col-md-6')
        for i in agents:
            temp = i.text.split(':')
            if len(temp) > 1:
                fullDict['Registered Agent'][temp[0]] = temp[1]
            else:
                fullDict['Registered Agent'][temp[0]] = ''
        officers = test.find_elements_by_tag_name('td')
        for i in range(0, len(officers), 5):
            fullDict['Officers']['Title'] = officers[i].text
            fullDict['Officers']['Governors Type'] = officers[i + 1].text
            fullDict['Officers']['Name'] = officers[i + 3].text + ' ' + officers[i + 4].text
        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)
        return self.scrapeData(driver)
