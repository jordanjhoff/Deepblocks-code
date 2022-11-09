from selenium import webdriver
import time

class Montana_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://www.mtsosfilings.gov/mtsos-master/service/create.html?service=registerItemSearch"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_xpath('//*[@id="QueryString"]')
        text.send_keys(entity_name)
        temp = driver.find_elements_by_class_name('appReceiveFocus')
        submit = temp[2]
        submit.click()
        return driver

    def scrapeData(self, driver, fullDict):
        # finds and navigates to the link for the first entity
        time.sleep(4)
        temp = driver.find_elements_by_class_name('appReceiveFocus')
        link = temp[3]
        link.click()

        # assigns strings to keys and values for the dictionary depending on their position on the page
        keys = driver.find_elements_by_class_name('appAttrLabel')
        values = driver.find_elements_by_class_name('appAttrValue')
        for i in range(len(keys)):
            if keys[i].text == '':
                fullDict['Information']['Name'] = values[i].text
            elif keys[i].text.lower() == 'name':
                pass
            else:
                fullDict['Information'][keys[i].text] = values[i].text

        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        fullDict = {
            'Information': {}
        }
        driver = self.findDetailsPage(driver, entity_name)
        driver.implicitly_wait(3)
        return self.scrapeData(driver, fullDict)