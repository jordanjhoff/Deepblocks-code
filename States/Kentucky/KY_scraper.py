from selenium import webdriver

class Kentucky_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://web.sos.ky.gov/ftsearch/"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_FTUC_TextBox1"]')
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_FTUC_Button2"]')
        submit.click()

        # finds and navigates to the link for the first entity
        try:
            link = driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_FTUC_pOrglist"]/table/tbody/tr[2]/td[1]/a')
            link.click()
        except:
            pass
        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # scrapes information
        fullDict = {
            'Information': {},
            'Officers': {},
        }

        tbody = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_FTUC_pInfo"]/table/tbody')
        info = tbody.find_elements_by_tag_name('tr')
        for i in range(1, len(info)):
            fullDict['Information'][driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_FTUC_pInfo"]/table/tbody/tr[' + str(
                    i) + ']/td[2]').text] = driver.find_element_by_xpath(
                '//*[@id="ctl00_ContentPlaceHolder1_FTUC_pInfo"]/table/tbody/tr[' + str(i) + ']/td[3]').text
        try:
            table = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_FTUC_pInitial"]/table[1]/tbody')
            officers = table.find_elements_by_tag_name('td')
            for i in range(0, len(officers), 3):
                fullDict['Officers'][officers[i + 1].text + ' (Officer # ' + str(int(i / 3 + 1)) + ')'] = officers[
                    i + 2].text
        except Exception:
            pass
        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)