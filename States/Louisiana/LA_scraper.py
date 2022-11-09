from selenium import webdriver
import time

class Louisiana_Bot():
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    def initializeSelenium(self, chromedriver_location):
        # calls createUrlFromName with input
        url = "https://coraweb.sos.la.gov/CommercialSearch/CommercialSearch.aspx"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    # navigates to the company specific page on the website
    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_txtEntityName"]')
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="ctl00_cphContent_btnSearch"]')
        submit.click()

        # finds and navigates to the link for the first entity
        htmls = driver.find_element_by_tag_name('html')
        if '<input type="submit" name="ctl00$cphContent$grdSearchResults_EntityNameOrCharterNumber$ctl03$btnView' \
           'Details" value="Details" id="ctl00_cphContent_grdSearchResults_EntityNameOrCharterNumber_ct' in \
                htmls.get_attribute('innerHTML'):
            try:
                link = driver.find_element_by_xpath(
                    '//*[@id="ctl00_cphContent_grdSearchResults_EntityNameOrCharterNumber_ctl02_btnViewDetails"]')
                link.click()
            except Exception:
                link = driver.find_element_by_xpath(
                    '//*[@id="ctl00_cphContent_grdSearchResults_EntityNameOrCharterNumber_ctl03_btnViewDetails"]')
                link.click()
                pass
        return driver

    # Scrapes all general information about the company as well as information on specific agents and officers
    def scrapeData(self, driver):
        # scrapes information
        fullDict = {}
        information = {}
        officers = {}
        agents = {}
        time.sleep(1)

        info = driver.find_elements_by_tag_name('tr')
        for i in info:
            if i.text == ' ':
                info.remove(i)
        filtered = []
        split_lists = []
        for i in info:
            temp_text = i.text
            colon_count = i.text.count(':')
            if colon_count > 0:
                if 'Officer(s) Additional Officers' not in i.text:
                    if colon_count > 1:
                        split_lines = temp_text.split('\n')
                        split_lists.append(split_lines)
                        if split_lines not in split_lists:
                            for line in split_lines:
                                filtered.append(line.strip())
                    else:
                        filtered.append(temp_text.strip())
        agent_names = []
        agent_addresses = []
        officer_names = []
        officer_titles = []
        officer_addresses = []
        officer = False

        for i in filtered:
            index = int(i.find(':'))
            if 'agent' in i.lower():
                agent_names.append(i[index + 1:len(i)])
            elif 'officer' in i.lower():
                officer = True
                officer_names.append(i[index + 1:len(i)])
            elif 'title' in i.lower():
                officer_titles.append(i[index + 1:len(i)])
            elif 'address' in i.lower():
                if officer:
                    officer_addresses.append(i[index + 1:len(i)])
                else:
                    agent_addresses.append(i[index + 1:len(i)])
            elif 'city, state, zip' in i.lower():
                if officer:
                    officer_addresses[len(officer_addresses) - 1] = officer_addresses[
                                                                        len(officer_addresses) - 1] + ', ' + i[index + 1:len(i)]
                else:
                    agent_addresses[len(agent_addresses) - 1] = agent_addresses[len(agent_addresses) - 1] + ', ' + i[
                                                                                                      index + 1:len(i)]
            else:
                information[i[0: index]] = i[index + 1: len(i)]

        agents['Names'] = agent_names
        agents['Addresses'] = agent_addresses
        officers['Names'] = officer_names
        officers['Titles'] = officer_titles
        officers['Addresses'] = officer_addresses

        fullDict['Agents'] = agents
        fullDict['Officers'] = officers
        fullDict["Information"] = information
        driver.quit()
        return fullDict

    def run_script(self):
        entity_name = self.entity_name
        chromedriver_location = self.chromedriver_location
        driver = self.initializeSelenium(chromedriver_location)
        driver = self.findDetailsPage(driver, entity_name)

        return self.scrapeData(driver)
