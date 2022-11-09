from selenium import webdriver
import time

class Virginia_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://cis.scc.virginia.gov/"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_id("txtEntityName")
        text.send_keys(entity_name)
        time.sleep(1)
        submit = driver.find_element_by_css_selector("[onclick^='PerfmEntitySearch()']")
        # submit.click()
        driver.execute_script("arguments[0].click()", submit)
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
        #   '//*[@id="divUccSearch"]/div[4]/button'))).click()

        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="grid_businessList"]/tbody/tr[1]/td[1]/a')
        link.click()

        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # scrapes information and officers
        allinfo = {
            'Information': {},
            'Agents': {},
            'Officers': {}

        }
        for i in range(1, 9):
            if driver.find_element_by_xpath('/html/body/div[1]/section/div[3]/div[1]/div/div/div/div[2]/div[' + str(
                    i) + ']/div[4]').text == 'Annual Report Due Date:':
                allinfo['Information']['Annual Report Due Date:'] = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[1]/div/div/div/div[2]/div[6]/div[5]').text
            else:
                allinfo['Information'][driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[1]/div/div/div/div[2]/div[' + str(
                        i) + ']/div[1]').text] = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[1]/div/div/div/div[2]/div[' + str(i) + ']/div[2]').text
                allinfo['Information'][driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[1]/div/div/div/div[2]/div[' + str(
                        i) + ']/div[3]').text] = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[1]/div/div/div/div[2]/div[' + str(i) + ']/div[4]').text
            for i in range(2, 5):
                allinfo['Agents'][driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[2]/div/div/div/div[' + str(
                        i) + ']/div[1]').text] = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[2]/div/div/div/div[' + str(i) + ']/div[2]').text
                allinfo['Agents'][driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[2]/div/div/div/div[' + str(
                        i) + ']/div[3]').text] = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[2]/div/div/div/div[' + str(i) + ']/div[4]').text
                allinfo['Agents'][driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[3]/div/div/div/div[2]/div[1]').text] = driver.find_element_by_xpath(
                    '/html/body/div[1]/section/div[3]/div[3]/div/div/div/div[2]/div[2]').text
        title = []
        director = []
        name = []
        address = []
        updated = []
        tableItems = driver.find_elements_by_tag_name('td')
        for i in range(0, len(tableItems), 5):
            title.append(tableItems[i].text)
            director.append(tableItems[i + 1].text)
            name.append(tableItems[i + 2].text)
            address.append(tableItems[i + 3].text)
            updated.append(tableItems[i + 4].text)

        allinfo['Officers']['Title'] = title
        allinfo['Officers']['Director?'] = director
        allinfo['Officers']['Name'] = name
        allinfo['Officers']['Date Updated'] = updated
        allinfo['Officers']['Address'] = address
        driver.quit()
        return allinfo

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)
