from selenium import webdriver
import time

class Wyoming_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        url = "https://wyobiz.wyo.gov/Business/FilingSearch.aspx"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_id("MainContent_txtFilingName")
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="MainContent_cmdSearch"]')
        submit.click()
        driver.implicitly_wait(3)
        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="Ol1"]/li[1]/a')
        link.click()
        time.sleep(2)

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # scrapes information
        fullDict = {
            'Information': {},
            'Officers': {
                'Name': [],
                'Address': [],
                'Organization': []
            }
        }
        labels = driver.find_elements_by_class_name('fieldLabel')
        data = driver.find_elements_by_class_name('fieldData')
        labelIndex = 0
        datumIndex = 0
        while datumIndex < len(data):
            if data[datumIndex].text:
                fullDict['Information'][labels[labelIndex].text] = data[datumIndex].text
                datumIndex += 1
                labelIndex += 1
            else:
                datumIndex += 1
        parties = driver.find_element_by_xpath('//*[@id="accordion2"]/div/div[7]/a')
        parties.click()
        time.sleep(1)
        rows = driver.find_elements_by_tag_name('ol')
        for row in rows:
            fullDict['Officers']['Name'].append(row.find_element_by_class_name('resHist1').text)
            org = row.find_element_by_class_name('resHist2').text.split(': ')
            address = row.find_element_by_class_name('resHist3').text.split(': ')
            if len(address) > 1:
                fullDict['Officers']['Address'].append(address[1])
            if len(org) > 1:
                fullDict['Officers']['Organization'].append(org[1])

        titles = []
        temp = fullDict['Officers']['Name']
        for i in range(len(temp)):
            titles.append(temp[i][temp[i].find('(') + 1:temp[i].find(')')])
            temp[i] = temp[i][:temp[i].find('(')].strip()
        fullDict['Officers']['Titles'] = titles
        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)
        driver.implicitly_wait(3)
        return self.scrapeData(driver)
