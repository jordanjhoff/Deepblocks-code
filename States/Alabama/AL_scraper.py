from selenium import webdriver

class Alabama_Bot():
    # Pass the entity name and the location of chromedriver on your computer to initialize
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "http://arc-sos.state.al.us/CGI/corpname.mbr/input"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_xpath('//*[@id="block-sos-content"]/div/div/div[1]/form/div[1]/input')
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="block-sos-content"]/div/div/div[1]/form/div[6]/input')
        submit.click()
        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="block-sos-content"]/div/div/div/table/tbody/tr[1]/td[2]/a')
        link.click()
        return driver

    def scrapeData(self, driver):
        # creates dictionary
        fullDict = {}
        fullDict['Information'] = {}
        headers = driver.find_elements_by_class_name('aiSosDetailHead')

        for i in range(len(headers)):
            if i == 0:
                fullDict['Information']['Entity Name'] = headers[i].text
            else:
                fullDict[headers[i].text] = {}

        tables = driver.find_elements_by_tag_name('tbody')
        for i in range(len(tables)):
            rows = tables[i].find_elements_by_tag_name('td')
            for j in range(0, len(rows) - 1, 2):
                if i == 0:
                    if rows[j].text in fullDict['Information'].keys():
                        temp = fullDict['Information'][rows[j].text]
                        if isinstance(temp, list):
                            temp.append(rows[j + 1].text)
                            fullDict['Information'][rows[j].text] = temp
                        else:
                            fullDict['Information'][rows[j].text] = [temp, rows[j + 1].text]
                    else:
                        fullDict['Information'][rows[j].text] = rows[j + 1].text
                else:
                    if rows[j].text in fullDict[headers[i].text].keys():
                        temp = fullDict[headers[i].text][rows[j].text]
                        if isinstance(temp, list):
                            temp.append(rows[j + 1].text)
                            fullDict[headers[i].text][rows[j].text] = temp
                        else:
                            fullDict[headers[i].text][rows[j].text] = [temp, rows[j + 1].text]
                    else:
                        fullDict[headers[i].text][rows[j].text] = rows[j + 1].text

        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)

