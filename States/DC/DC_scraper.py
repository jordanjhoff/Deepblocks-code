from selenium import webdriver
import time

class DC_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://corponline.dcra.dc.gov/Account.aspx/LogOn?ReturnUrl=%2fHome.aspx"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    def login(self, driver):
        username = driver.find_element_by_id('txtUsername')
        password = driver.find_element_by_id('txtPassword')
        username.send_keys("deepblocks1")
        password.send_keys("deepblocks")


        submit = driver.find_element_by_xpath('//*[@id="btnSubmit"]')
        submit.click()

        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="tabList"]/li[1]/a').click()
        time.sleep(1)
        return driver

    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_id("BizEntitySearch_String")
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="SimpleSearch"]')
        submit.click()
        driver.implicitly_wait(3)

        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="BizEntitySearch_SearchResultsTable"]/tbody/tr[1]/td[2]/a')
        link.click()
        time.sleep(2)

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        fullDict = {}
        for i in range(1, 4):
            section = driver.find_element_by_xpath('//*[@id="tab630View"]/div/fieldset[' + str(i) + ']')

            header = section.find_element_by_class_name('legendhead')
            fullDict[header.text] = {}
            keys = section.find_elements_by_class_name('spanreadonlylabel')
            values = section.find_elements_by_class_name('spanreadonlyvalue')
            for i in range(len(keys)):
                fullDict[header.text][keys[i].text] = values[i].text

        # scrapes officer information
        officerTab = driver.find_element_by_xpath('//*[@id="tab633"]/a')
        officerTab.click()
        time.sleep(1)
        section = driver.find_element_by_xpath('//*[@id="tab633View"]/div/fieldset')
        fullDict['Officers'] = {
            'Titles': [],
            'Names': [],
            'Addresses': [],
            'Executing Officers': [],
            'File Numbers': []
        }
        tbody = section.find_element_by_xpath('//*[@id="EntityContactListTable"]/tbody')
        rows = tbody.find_elements_by_tag_name('tr')
        for row in rows:
            items = row.find_elements_by_tag_name('td')
            fullDict['Officers']['Titles'].append(items[0].text)
            fullDict['Officers']['Names'].append(items[1].text)
            fullDict['Officers']['Addresses'].append(items[2].text)
            fullDict['Officers']['Executing Officers'].append(items[3].text)
            fullDict['Officers']['File Numbers'].append(items[4].text)

        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.login(driver)
        driver = self.findDetailsPage(driver, entity_name)

        driver.implicitly_wait(3)
        return self.scrapeData(driver)
