from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MI_scraper():
    def __init__(self, entity_name, chrome_driver_location):
        self.entity_name = entity_name
        self.chrome_driver_location = chrome_driver_location

    def create_selenium_instance(self, url, chrome_driver_location):
        driver = webdriver.Chrome(executable_path=chrome_driver_location)
        driver.get(url)
        driver.implicitly_wait(2000)
        return driver

    # Inputs the company name in the search bar and navigates to the results page
    def search_for_entity(self, driver, entity_name, text_box_id, search_button_id):
        text = driver.find_element_by_id(text_box_id)
        text.send_keys(entity_name)
        wait = WebDriverWait(driver, 30)
        submit = wait.until(EC.element_to_be_clickable((By.ID, search_button_id)))
        driver.implicitly_wait(8000)
        try:
            submit.click()
        except:
            driver.implicitly_wait(5000)
            submit.click()
        driver.implicitly_wait(5000)
        return driver

    # Clicks on the first entity on the results page to go to the company specific page on the website
    def first_result_page(self, driver, xpath):
        link = driver.find_element_by_xpath(xpath)
        driver.implicitly_wait(8000)
        link.click()
        driver.implicitly_wait(5000)
        return driver

    # Separates the pages different sections as elements in a list
    def get_sections(self, driver):
        sections = driver.find_element_by_id("content").find_elements_by_class_name('TableBorderGray')
        return sections

    # Gets all the general information about the company
    def get_entity_type(self, section):
        entity_type = {}
        keys = section.find_elements_by_tag_name('strong')
        values = section.find_elements_by_tag_name('span')
        keys.insert(0, values.pop(0))
        for i in range(len(keys)):
            entity_type[keys[i].text.replace(':', '')] = values[i].text
        return entity_type

    # Gets all registered agent information (name, address, etc.)
    def get_registered(self, section):
        registered_agent = {}
        registered_office = {}
        registered = []
        tables = section.find_elements_by_tag_name('table')
        for i in range(len(tables)):
            tds = tables[i].find_elements_by_tag_name('td')
            keys = []
            values = []
            for td in tds:
                if ":" in td.text:
                    keys.append(td.text)
                else:
                    values.append(td.text)
            keys.pop(0)
            if i == 0:
                for j in range(len(keys)):
                    if values[j] == '':
                        values[j] = values[j].replace('', 'NONE')
                    registered_agent[keys[j].replace(':', '')] = values[j]
            elif i == 1:
                for j in range(len(keys)):
                    registered_office[keys[j].replace(':', '')] = values[j].replace('', 'NONE')
        registered.append(registered_agent)
        registered.append(registered_office)

        return(registered)

    # Gets information on officers and directors in the company (name, address, etc.)
    def get_officers_and_directors(self, section):
        officers_and_directors = {}
        table = section.find_element_by_tag_name('table')
        rows = table.find_elements_by_class_name('GridRow')
        names = []
        titles = []
        addresses = []
        for row in rows:
            cells = row.find_elements_by_tag_name('td')
            names.append(cells[1].text)
            titles.append(cells[0].text)
            addresses.append(cells[2].text)
        officers_and_directors["Names"] = names
        officers_and_directors["Titles"] = titles
        officers_and_directors["Addresses"] = addresses
        return officers_and_directors

    def run_script(self):
        entity_name = self.entity_name
        chrome_driver_location = self.chrome_driver_location
        driver = self.create_selenium_instance(
            "https://cofs.lara.state.mi.us/SearchApi/Search/Search", chrome_driver_location)
        search_results = self.search_for_entity(driver, entity_name, "txtEntityName", "SearchSubmit")
        first_result_page = self.first_result_page(search_results,
                                                   "/html/body/div[2]/div[3]/div[1]/div[3]/div/div/div[2]/table[1]/tbody/tr[1]/td[2]/a")
        entity_data = {}

        # goes through each section and checks for keywords and if its present it makes a dictionary for that type of information
        for section in self.get_sections(first_result_page):
            if "entity type" in section.text.lower():
                entity_data["Information"] = self.get_entity_type(section)
            if "the name and address of the resident agent" in section.text.lower():
                values = self.get_registered(section)
                entity_data["Registered Agent Name and Address"] = values[0]
                entity_data["Registered Office Mailing Address"] = values[1]
            if "officers and directors" in section.text.lower():
                entity_data["Officers and Directors"] = self.get_officers_and_directors(section)

        return entity_data