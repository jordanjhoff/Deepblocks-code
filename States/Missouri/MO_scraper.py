from selenium import webdriver
import time

class Missouri_Bot():
    # Pass the entity name and the location of chromedriver on your computer to initialize
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://bsd.sos.mo.gov/search"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        time.sleep(4)
        text = driver.find_element_by_xpath('//*[@id="aef11785-d8f2-c109-bd4d-c49d3906e3e3"]')
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath(
            '//*[@id="content"]/regsys-search/div/div/div/div[1]/aside/regsys-form-render/div/div[3]/div[1]/div[2]/div/regsys-reactive-button/button')
        submit.click()
        time.sleep(3)
        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath(
            '//*[@id="content"]/regsys-search/div/div/div/div[2]/section/div/mat-table/mat-row/mat-cell[6]/regsys-reactive-button/button')
        driver.execute_script("arguments[0].click();", link)
        time.sleep(2)

        return driver

    def scrapeData(self, driver):
        # creates dictionary
        fullDict = {
            'Profile': {},
            'Addresses': {},
            'Officers': {
                'Name': [],
                'Title': [],
                'Effective From': []
            },
            'Agents' : {
                'Name': [],
                'Effective From': []
            }
        }
        # scrapes profile
        profile = driver.find_element_by_xpath('// *[ @ id = "tab-catalog-entity-profile-panel"]/regsys-catalog-entity-details/dl')
        keys = profile.find_elements_by_class_name('rs-field-label')
        values = profile.find_elements_by_class_name('rs-regular-text')
        for i in range(len(keys)):
            fullDict['Profile'][keys[i].text] = values[i].text
            # scrapes addresses, if any
        profile = driver.find_element_by_xpath('//*[@id="tab-catalog-entity-profile-panel"]/regsys-entity-addresses/dl')
        keys = profile.find_elements_by_class_name('rs-field-label')
        values = profile.find_elements_by_class_name('rs-regular-text')
        for i in range(len(keys)):
            fullDict['Addresses'][keys[i].text] = values[i].text
            # scrapes Officers and agents, if any
        try:
            partiesButton = driver.find_element_by_xpath('//*[@id="tab-catalog-relationships"]')
            driver.execute_script("arguments[0].click();", partiesButton)
            time.sleep(1)
            table = driver.find_element_by_xpath('//*[@id="tab-catalog-relationships-panel"]')
            parties = table.find_elements_by_tag_name('p')
            for i in range(0, len(parties), 3):
                fullDict['Officers']['Name'].append(parties[i].text)
                fullDict['Officers']['Title'].append(parties[i + 1].text)
                fullDict['Officers']['Effective From'].append(parties[i + 2].text)
        except Exception:
            pass
        
        # makes a temporary list to hold the titles from the officers dictionary
        titles = []
        for key, val in fullDict['Officers'].items():
            if key == 'Title':
                for i in range(len(val)):
                    titles.append(val[i])

        # takes any agents out of officers and puts the information into agents
        if titles:
            for i in range(len(titles)):
                if 'agent' in titles[i].lower():
                    del fullDict['Officers']['Title'][i]
                    fullDict['Agents']['Name'].append(fullDict['Officers']['Name'].pop(i))
                    fullDict['Agents']['Effective From'].append(fullDict['Officers']['Effective From'].pop(i))

        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        driver.implicitly_wait(3)

        return self.scrapeData(driver)
