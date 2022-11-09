from selenium import webdriver
import time

'''IMPORTANT NOTE: BotID defense on the website that rejects requests to URL'''

class Alaska_Bot():
    # Pass the entity name and the location of chromedriver on your computer to initialize
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://www.commerce.alaska.gov/cbp/main/search/entities"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)
        driver.delete_all_cookies()

        # get URL
        driver.get(url)

        return driver

    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_xpath('//*[@id="EntityName"]')
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="search"]')
        submit.click()

        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('/html/body/div/div[1]/main/article/form/div[2]/table/tbody/tr[1]/td[2]/a')
        link.click()
        return driver

    # scrapes information from the page
    def scrapeData(self, driver):
        fullDict = {
            'Information': {},
            'Officers': {},
        }

        time.sleep(5)
        key = driver.find_elements_by_tag_name('dt')
        value = driver.find_elements_by_tag_name('dd')
        for i in range(3, len(key)):
            fullDict['Information'][key[i].text] = value[i].text

        grid = driver.find_element_by_id('officialsGrid')
        officials = grid.find_elements_by_tag_name('tr')
        names = []
        titles = []
        for i in range(1, len(officials)):
            officer = officials[i].text.split()
            if len(officer) == 3:
                names.append(officer[0] + ' ' + officer[1])
                titles.append(officer[2])
            else:
                names.append(officer[0] + ' ' + officer[1])
                titles.append(officer[2] + ' ' + officer[3])

        fullDict['Officers']['Names'] = names
        fullDict['Officers']['Titles'] = titles
        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)
