from selenium import webdriver

class California_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.entity_type = "CORP"
        self.chromedriver_location = chromedriver_location

    # goes to the company specific page by creating the page's URL using the entity name/type
    def create_URL(self, entity_type, entity_name):
        temp_name = entity_name.replace(" ", "+")
        return "https://businesssearch.sos.ca.gov/CBS/SearchResults?filing=&SearchType=" + entity_type + "&SearchCriteria=" + temp_name + "&SearchSubType=Keyword"

    def initializeSelenium(self, chromedriver_location, url):
        # calls createUrlFromName with input

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        table = driver.find_element_by_tag_name("tbody")
        tbody = table.find_elements_by_tag_name("tr")
        row = driver.find_element_by_xpath('//*[@id="enitityTable"]/tbody/tr[1]')

        # finds entity num
        entityNum = row.find_element_by_tag_name("td").text
        entityDict = {
            'Information': {}
        }
        entityDict['Information']['Entity Number'] = entityNum

        dataButton = row.find_element_by_tag_name("button")
        entityDict['Information']['Entity Name'] = dataButton.text
        dataButton.click()

        # finds all data on details page
        for i in range(1, 7):
            key = driver.find_element_by_xpath(
                '//*[@id="maincontent"]/div[3]/div[1]/div[' + str(i) + ']/div[1]/strong').text
            entityDict['Information'][key] = driver.find_element_by_xpath(
                '//*[@id="maincontent"]/div[3]/div[1]/div[' + str(i) + ']/div[2]').text
        driver.quit()
        return entityDict

    def run_script(self):
        entity_name = self.entity_name
        entity_type = self.entity_type
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location, self.create_URL(entity_type, entity_name))

        return self.scrapeData(driver)
