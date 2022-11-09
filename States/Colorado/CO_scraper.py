from selenium import webdriver
import time


class Colorado_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://www.sos.state.co.us/biz/BusinessEntityCriteriaExt.do?resetTransTyp=Y"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)
        time.sleep(2)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_xpath(
            '//*[@id="application"]/table/tbody/tr/td[2]/table/tbody/tr[3]/td/form/table[1]/tbody/tr[5]/td/table/tbody/tr/td/table/tbody/tr/td[2]/font/input')
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath(
            '//*[@id="application"]/table/tbody/tr/td[2]/table/tbody/tr[3]/td/form/table[2]/tbody/tr/td[1]/input')
        submit.click()
        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="box"]/table/tbody/tr[2]/td[2]/a')
        link.click()
        time.sleep(2)
        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # creates dictionary
        fullDict = {}
        container = driver.find_element_by_xpath(
            '//*[@id="application"]/table/tbody/tr/td[2]/table/tbody/tr[3]/td/form/table[1]/tbody/tr[1]/td/table/tbody')
        tbody = container.find_elements_by_tag_name('tbody')
        for t in tbody:
            header = t.find_element_by_tag_name('th')
            rows = t.find_elements_by_tag_name('td')
            fullDict[header.text] = {}
            for i in range(0, len(rows), 2):
                if i + 1 < len(rows):
                    fullDict[header.text][rows[i].text] = rows[i + 1].text
        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        driver.implicitly_wait(3)
        return self.scrapeData(driver)
