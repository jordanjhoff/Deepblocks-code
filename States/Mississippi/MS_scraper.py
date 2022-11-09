from selenium import webdriver
import time

class Mississippi_Bot():
    # Pass the entity name and the location of chromedriver on your computer to initialize
    def __init__(self, entity_name, chromedriver_location):
        self.entity_name = entity_name
        self.chromedriver_location = chromedriver_location

    
    def initializeSelenium(self, chromedriver_location):
        url = "https://corp.sos.ms.gov/corp/portal/c/page/corpBusinessIdSearch/portal.aspx?#clear=1"

        # starts Selenium
        driver = webdriver.Chrome(executable_path=chromedriver_location)

        # get URL
        driver.get(url)

        return driver

    def findDetailsPage(self, driver, entity_name):
        # inputs information to search
        text = driver.find_element_by_id("businessNameTextBox")
        text.send_keys(entity_name)
        submit = driver.find_element_by_xpath('//*[@id="businessNameSearchButton"]')
        submit.click()
        driver.implicitly_wait(3)
        # finds and navigates to the link for the first entity
        link = driver.find_element_by_xpath('//*[@id="businessSearchResultsDiv"]/table/tbody/tr[1]/td[6]/a')
        link.click()
        time.sleep(2)

        return driver

    def scrapeData(self, driver):  
        # scrapes information from the page
        fullDict = {
            'Name History': {},
            'Business Information': {},
            'Agents': {},
            'Officers': {}
        }
        nameHistoryHeader = driver.find_element_by_xpath('//*[@id="printDiv2"]/div[2]/table/tbody/tr[1]/td[1]').text
        nameTypeHeader = driver.find_element_by_xpath('//*[@id="printDiv2"]/div[2]/table/tbody/tr[1]/td[3]').text
        fullDict['Name History'][nameHistoryHeader] = []
        fullDict['Name History'][nameTypeHeader] = []

        tbody = driver.find_element_by_xpath('//*[@id="printDiv2"]/div[2]/table/tbody')
        tr = tbody.find_elements_by_tag_name('tr')
        for i in range(1, len(tr)):
            td = tr[i].find_elements_by_tag_name('td')
            fullDict['Name History'][nameHistoryHeader].append(td[0].text)
            fullDict['Name History'][nameTypeHeader].append(td[2].text)

        table_number = 3 # number of tables decreases if the agents table doesnt exist
        # scrapes business information
        tbody = driver.find_element_by_xpath('//*[@id="printDiv2"]/table[1]/tbody')
        tr = tbody.find_elements_by_tag_name('tr')
        for i in range(1, len(tr)):
            td = tr[i].find_elements_by_tag_name('td')
            fullDict['Business Information'][td[0].text] = td[1].text

        # scrapes registered agent table
        wrapper = driver.find_element_by_xpath('//*[@id="printDiv2"]')
        if 'table class="subTable"' in wrapper.get_attribute('innerHTML'):
            try:
                agent_tbody = driver.find_element_by_xpath('//*[@id="printDiv2"]/table[2]/tbody')
                agent_trs = agent_tbody.find_elements_by_tag_name('tr')
                agent_names = []
                agent_addresses = []
                if agent_trs[0].find_element_by_tag_name('td').text == 'Name':
                    for i in range(len(agent_trs)):
                        if (i != 0):
                            agent_tds = agent_trs[i].find_elements_by_tag_name('td')
                            for td in agent_tds:
                                agent_names.append(td.text[0: td.text.index('\n')])
                                agent_addresses.append(td.text[td.text.index('\n') + 1:])
                    fullDict['Agents']['Names'] = agent_names
                    fullDict['Agents']['Addresses'] = agent_addresses
            except Exception:
                table_number = 2
                pass

        # scrapes officers and directors
        wrapper = driver.find_element_by_xpath('//*[@id="printDiv2"]')
        if '<table class="subTable" style="width:100%;">' in wrapper.get_attribute('innerHTML'):
            try:
                officer_tbody = driver.find_element_by_xpath('//*[@id="printDiv2"]/table[2]/tbody')
                officer_trs = officer_tbody.find_elements_by_tag_name('tr')
                officer_names = []
                officer_addresses = []
                officer_titles = []
                if officer_trs[0].find_element_by_tag_name('td').text == 'Name':
                    for i in range(1, len(officer_trs)):
                        main_tr = driver.find_element_by_xpath('//*[@id="printDiv2"]/table['+str(table_number)+']/tbody/tr['+str(i+1)+']')
                        officer_tds = main_tr.find_elements_by_tag_name('td')
                        for j in range(len(officer_tds)):
                            if j == 0:
                                officer_names.append(officer_tds[j].text[0: officer_tds[j].text.index('\n')])
                                officer_addresses.append(officer_tds[j].text[officer_tds[j].text.index('\n') + 1:])
                            elif j == 2:
                                officer_titles.append(officer_tds[j].text)
                    fullDict['Officers']['Names'] = officer_names
                    fullDict['Officers']['Addresses'] = officer_addresses
                    fullDict['Officers']['Titles'] = officer_titles
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