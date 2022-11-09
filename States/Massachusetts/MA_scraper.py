from selenium import webdriver

class Massachusetts_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://corp.sec.state.ma.us/corpweb/CorpSearch/CorpSearch.aspx"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_id("MainContent_txtEntityName")
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="MainContent_btnSearch"]')
        submit.click()

        # finds and navigates to the link for the first entity
        time.sleep(3)
        link = driver.find_element_by_xpath(
            '//*[@id="MainContent_SearchControl_grdSearchResultsEntity"]/tbody/tr[2]/th/a')
        link.click()

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # scrapes information
        fullDict = {
            'Information': {},
            'Officers': {}
        }
        tables = driver.find_elements_by_class_name('TableBorderGray')
        for i in range(len(tables) - 4):
            if "the name was changed from:" in tables[i].text.lower() \
                    or "if the business entity is organized wholly" in tables[i].text.lower()\
                    or "in addition to the manager(s)" in tables[i].text.lower()\
                    or "the name and business address of the person(s) authorized" in tables[i].text.lower()\
                    or "the name and business address of each manager" in tables[i].text.lower()\
                    or "the officers and directors of the corporation" in tables[i].text.lower():
                pass
            elif "\n" in tables[i].text or "\r" in tables[i].text:
                row = tables[i].text.splitlines()
                fullDict[row[0]] = {}
                for i in range(1, len(row)):
                    values = row[i].split(':')
                    for j in range(0, len(values), 2):

                        if (j + 1 < len(values)):
                            if 'city or town, state' in values[j].strip().lower():
                                fullDict[row[0]]['Address'] = fullDict[row[0]]['Address'] + ', ' + values[j+1]
                            else:
                                fullDict[row[0]][values[j].strip()] = values[j + 1]
            else:
                row = tables[i].text.split(':')
                fullDict['Information'][row[0].strip()] = row[1].strip()
        temp = driver.find_element_by_class_name('Grid')
        officers = temp.find_elements_by_class_name('GridRow')
        titles = []
        names = []
        addresses = []
        otherInfo = []
        for i in officers:
            titles.append(i.find_element_by_tag_name('th').text)
            otherInfo.append(i.find_elements_by_tag_name('td'))
        for i in otherInfo:
            names.append(i[0].text)
            addresses.append(i[1].text)
        fullDict['Officers']['Title'] = titles
        fullDict['Officers']['Name'] = names
        fullDict['Officers']['Address'] = addresses
        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)
        return self.scrapeData(driver)