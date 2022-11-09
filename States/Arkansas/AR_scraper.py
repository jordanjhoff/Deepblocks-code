from selenium import webdriver

class Arkansas_Bot():
    # Pass the entity name and the location of chromedriver on your computer to initialize
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://www.sos.arkansas.gov/corps/search_corps.php"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_name("corp_name")
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="mainContent"]/form/table/tbody/tr[11]/td/font/input')
        submit.click()

        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="mainContent"]/table[3]/tbody/tr[2]/td[1]/font/div/a')
        link.click()

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        fullDict = {
            'Information': {},
            'Addresses': {},
        }

        for i in range(2, 16):
            key = driver.find_element_by_xpath('//*[@id="mainContent"]/table[2]/tbody/tr[' + str(i) + ']/td[1]/font')
            value = driver.find_element_by_xpath('//*[@id="mainContent"]/table[2]/tbody/tr[' + str(i) + ']/td[2]/font')
            if i == 8 or i == 10 or i == 14:
                fullDict['Addresses'][key.text] = value.text
            else:
                fullDict['Information'][key.text] = value.text
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)
