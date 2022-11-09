from selenium import webdriver

class Pennsylvania_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://www.corporations.pa.gov/search/corpsearch"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_name("ctl00$MainContent$txtSearchTerms")
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="btnSearch"]')
        submit.click()

        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="lnkBEName"]')
        link.click()

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # scrapes information and officers
        # scrapes information
        fullDict = {
            'Information': {}
        }
        for i in range(1, 10):
            key = driver.find_element_by_xpath(
                '//*[@id="MainContent_pnlEntityDetails"]/div[3]/div/div[5]/div[1]/table/tbody/tr[' + str(
                    i) + ']/td[1]/b')
            value = driver.find_element_by_xpath(
                '//*[@id="MainContent_pnlEntityDetails"]/div[3]/div/div[5]/div[1]/table/tbody/tr[' + str(i) + ']/td[2]')
            fullDict['Information'][key.text] = value.text

        # checks amount of info tables
        htmls = driver.find_elements_by_class_name('col-md-6')
        counter = 0
        for html in htmls:
            if 'table class="table table-striped table-hover table-bordered"' in html.get_attribute('innerHTML'):
                counter += 1
        # if there are more than one table, then there is an officers table
        if counter > 1:
            officerTable = driver.find_element_by_xpath(
                '//*[@id="MainContent_pnlEntityDetails"]/div[3]/div/div[5]/div[2]/table/tbody')
            tableRows = officerTable.find_elements_by_tag_name('tr')
            names = []
            titles = []
            addresses = []
            iterator = 0
            # goes through each row and assigns values to lists
            for row in tableRows:
                all_tds = row.find_elements_by_tag_name('td')
                if len(all_tds) > 1:
                    if iterator % 3 == 0:
                        names.append(all_tds[1].text)
                    elif iterator % 3 == 1:
                        titles.append(all_tds[1].text)
                    elif iterator % 3 == 2:
                        addresses.append(all_tds[1].text)
                    iterator += 1
            officers = {
                "Names": names,
                "Titles": titles,
                "Addresses": addresses
            }
            fullDict["Officers"] = officers

        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)
