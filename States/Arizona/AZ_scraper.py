from selenium import webdriver
import time

class Arizona_Bot():
    # Pass the entity name and the location of chromedriver on your computer to initialize
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://ecorp.azcc.gov/EntitySearch/Index"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_id("quickSearch_BusinessName")
        text.send_keys(entity_name)
        submit = driver.find_element_by_id("btn_Search")
        submit.click()

        time.sleep(2)
        # finds and navigates to the link for the first entity listed on the results/search page
        link = driver.find_element_by_xpath('//*[@id="grid_resutList"]/tbody/tr/td[2]/a')
        link.click()

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        allinfo = {
            'Information': {},
            'Agents': {},
            'Officers': {}
        }
        for i in range(4, 11):
            allinfo['Information'][driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[' + str(i) + ']/div[1]').text] = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[' + str(i) + ']/div[2]').text
            allinfo['Information'][driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[' + str(i) + ']/div[3]').text] = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[' + str(i) + ']/div[4]').text
        for i in range(14, 20):
            allinfo['Agents'][driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[' + str(i) + ']/div[1]').text] = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[' + str(i) + ']/div[2]').text
        allinfo['Agents'][driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[14]/div[3]/label').text] = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[14]/div[4]').text
        allinfo['Agents'][driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[17]/div[3]/label').text] = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[17]/div[4]').text
        allinfo['Agents'][driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[18]/div[3]/label').text] = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[18]/div[4]').text
        tbody = driver.find_element_by_xpath('//*[@id="grid_principalList"]/tbody')

        title = []
        name = []
        address = []
        trs = tbody.find_elements_by_tag_name("tr")
        tds = 0
        for tr in trs:
            tds += tr.get_attribute('innerHTML').count('td')
        if tds > 2:
            for i in range(1, len(trs) + 1):
                title.append(
                    driver.find_element_by_xpath('//*[@id="grid_principalList"]/tbody/tr[' + str(i) + ']/td[1]').text)
            for i in range(1, len(tbody.find_elements_by_tag_name("tr")) + 1):
                name.append(
                    driver.find_element_by_xpath('//*[@id="grid_principalList"]/tbody/tr[' + str(i) + ']/td[2]').text)
            for i in range(1, len(tbody.find_elements_by_tag_name("tr")) + 1):
                address.append(
                    driver.find_element_by_xpath('//*[@id="grid_principalList"]/tbody/tr[' + str(i) + ']/td[4]').text)
        else:
            title.append(driver.find_element_by_xpath('//*[@id="grid_principalList"]/tbody/tr/td[1]').text)
            name.append(driver.find_element_by_xpath('//*[@id="grid_principalList"]/tbody/tr/td[1]').text)
            address.append(driver.find_element_by_xpath('//*[@id="grid_principalList"]/tbody/tr/td[1]').text)
        allinfo['Officers']['Title'] = title
        allinfo['Officers']['Name'] = name
        allinfo['Officers']['Address'] = address
        driver.quit()
        return allinfo

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)
