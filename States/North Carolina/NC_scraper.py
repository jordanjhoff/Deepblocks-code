import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# input
entity_name = input("Input Entity Name: ")

# calls createUrlFromName with input
url = "https://www.sosnc.gov/online_services/search/by_title/_Business_Registration"

# starts Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='/Users/Jonah1/Downloads/chromedriver')

# get URL
driver.get(url)
driver.implicitly_wait(2000)

# inputs information to search
text = driver.find_element_by_id("SearchCriteria")
text.send_keys(entity_name)
wait = WebDriverWait(driver, 30)
submit = wait.until(EC.element_to_be_clickable((By.ID, 'SubmitButton')))
driver.implicitly_wait(8000)
try:
    submit.click()
except:
    driver.implicitly_wait(5000)
    submit.click()
driver.implicitly_wait(5000)

# finds and navigates to the link for the first entity
link = driver.find_element_by_xpath('/html/body/div[2]/main/article/section/div/table/tbody/tr[1]/td[1]/b/a')

driver.implicitly_wait(8000)
link.click()
driver.implicitly_wait(5000)

entity_data = {}
time.sleep(5)
sections = driver.find_element_by_class_name("printFloatLeft").find_elements_by_tag_name('section')
for section in sections:
    this_section = {}
    section_title = section.find_element_by_tag_name('h2').text
    # print("Section Title: " + section_title) # Testing
    spans = []

    if "span" in section.get_attribute('innerHTML'):
        spans = section.find_elements_by_tag_name("span")
    else:
        # print(section.get_attribute('innerHTML')) # Testing
        spans = []

    subsec_content = ""
    subsec_title = ""
    subsec_titles = []
    for span in spans:
        if span.get_attribute('class') == "greenLabel":
            if subsec_title in subsec_titles:
                this_section[subsec_title + "(" + str(subsec_titles.count(subsec_title) + 1) + ")"] = subsec_content
                subsec_titles.append(subsec_title)
            else:
                this_section[subsec_title] = subsec_content
                subsec_titles.append(subsec_title)

            subsec_title = str(span.text).replace("\n", " ")
            subsec_content = ""
        else:
            subsec_content += str(span.text).replace("\n", " ")

    if subsec_title in subsec_titles:
        this_section[subsec_title + "(" + str(subsec_titles.count(subsec_title) + 1) + ")"] = subsec_content
    else:
        this_section[subsec_title] = subsec_content
    if "" in this_section.keys():
        del(this_section[""])
    entity_data[section_title] = this_section

# entity_data is the dictionary of dictionaries
pprint.pprint(entity_data, width=5, indent=0) # testing

driver.quit()

