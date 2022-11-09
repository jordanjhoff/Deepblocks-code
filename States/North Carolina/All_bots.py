from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NC_scraper():

    def __init__(self, entity_name, chrome_driver_location):
        self.entity_name = entity_name
        self.chrome_driver_location = chrome_driver_location

    def create_selenium_instance(self, chrome_driver_location):
        url = "https://www.sosnc.gov/online_services/search/by_title/_Business_Registration"
        driver = webdriver.Chrome(executable_path=chrome_driver_location)
        driver.get(url)
        return driver

    # Inputs the company name in the search bar and navigates to the results page
    def search_for_entity(self, driver, entity_name):
        text = driver.find_element_by_id("SearchCriteria")
        text.send_keys(entity_name)
        wait = WebDriverWait(driver, 30)
        submit = wait.until(EC.element_to_be_clickable((By.ID, "SubmitButton")))
        driver.implicitly_wait(8000)
        try:
            submit.click()
        except:
            driver.implicitly_wait(5000)
            submit.click()
        driver.implicitly_wait(5000)
        return driver

    # Clicks on the first entity on the results page to go to the company specific page on the website
    def first_result_page(self, driver):
        link = driver.find_element_by_xpath("/html/body/div[2]/main/article/section/div/table/tbody/tr[1]/td[1]/b/a")
        driver.implicitly_wait(8000)
        link.click()
        driver.implicitly_wait(5000)
        return driver

    # Separates the pages different sections as elements in a list
    def get_sections(self, driver):
        sections = driver.find_element_by_class_name("printFloatLeft").find_elements_by_tag_name('section')
        return sections

    # Gets the title of the section
    def get_section_title(self, section):
        section_title = section.find_element_by_tag_name('h2').text
        return section_title

    # Creates a list of spans for each section in the sections list, making sure that it exists first
    def get_spans(self, section):
        if "span" in section.get_attribute('innerHTML'):
            spans = section.find_elements_by_tag_name("span")
        else:
            spans = []

        return spans

    # Gets the title content of a section in the sections list
    def get_current_section_dict(self, section):
        this_section = {}
        subsection_content = ""
        subsection_title = ""
        subsection_titles = []
        for span in self.get_spans(section):
            if span.get_attribute('class') == "greenLabel":
                if subsection_title in subsection_titles:
                    this_section[subsection_title + "(" + str(
                        subsection_titles.count(subsection_title) + 1) + ")"] = subsection_content
                    subsection_titles.append(subsection_title)
                else:
                    this_section[subsection_title] = subsection_content
                    subsection_titles.append(subsection_title)
                subsection_title = str(span.text).replace("\n", " ")
                subsection_content = ""
            else:
                subsection_content += str(span.text).replace("\n", " ")
        if subsection_title in subsection_titles:
            this_section[
                subsection_title + "(" + str(subsection_titles.count(subsection_title) + 1) + ")"] = subsection_content
        else:
            this_section[subsection_title] = subsection_content
        if "" in this_section.keys():
            del (this_section[""])

        return this_section

    # Takes information from the main dictionary and creates a officer dictionary with more speific keys (name, title, address)
    def configure_officers(self, dict):
        if dict['Officers']:
            titles = []
            names = []
            addresses = []
            for key, val in dict['Officers'].items():
                titles.append(key)
                temp = val.split()
                address_start = -3
                for i in range(len(temp)):
                    if temp[i].isdigit() and address_start == -3:
                        address_start = i
                names.append(' '.join(temp[:address_start]))
                addresses.append(' '.join(temp[address_start:]))

            for i in range(len(names)):
                if names[i][names[i].rfind(' ') + 1:] in addresses[i]:
                    addresses[i] = addresses[i][:addresses[i].rfind(' ') + 6]
            del dict['Officers']
            officers = {
                'Names': names,
                'Titles': titles,
                'Addresses': addresses
            }
            dict['Officers'] = officers
        return dict


    def run_script(self):
        entity_name = self.entity_name
        chrome_driver_location = self.chrome_driver_location
        driver = self.create_selenium_instance(chrome_driver_location)
        search_results = self.search_for_entity(driver, entity_name)
        first_result_page = self.first_result_page(search_results,)
        entity_data = {}

        for section in self.get_sections(first_result_page):
            entity_data[self.get_section_title(section)] = self.get_current_section_dict(section)
        entity_data = self.configure_officers(entity_data)
        return entity_data
