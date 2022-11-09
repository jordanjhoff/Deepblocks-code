# difference between active and expired is that active has renew info and sometimes expired has an extra table that says "doing business as"
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

'''OUTPUT NOT FINISHED'''
# input
entity_name = input("Input Entity Name: ")

# for looping through files of entity names

# with open('FILE_NAME.csv') as name_file:
# reader = csv.reader(name_file delimiter='')
# for row in reader:
# name = row[0].strip()

# calls createUrlFromName with input
url = "https://secure.utah.gov/bes/"

# starts Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='/Users/Jonah1/Downloads/chromedriver')

# get URL
driver.get(url)
driver.implicitly_wait(2000)

#*********************************************************************


# inputs information to search
text = driver.find_element_by_id("name")
text.send_keys(entity_name)
wait = WebDriverWait(driver, 30)
submit = wait.until(EC.element_to_be_clickable((By.ID, 'searchByNameButton')))
driver.implicitly_wait(8000)
try:
    submit.click()
except:
    driver.implicitly_wait(5000)
    submit.click()
driver.implicitly_wait(5000)

# finds and navigates to the link for the first entity
link = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/a')

driver.implicitly_wait(8000)
link.click()
driver.implicitly_wait(5000)


time.sleep(5)

