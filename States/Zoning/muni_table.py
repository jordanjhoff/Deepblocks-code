'''This program finds all tables on a page and then prints the amount of keywords in the table, the keywords found in the table, and the table itself
   The tables are printed in descending order, with the table with the most keywords in it printed first.'''
import time
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException

'''Watches an element in the DOM (Document Object Model, which is a programming interface for HTML and XML documents 
and represents the page as nodes and objects, so programs can connect to the page and change the document's structure, 
style, and content) when the page initially loads, and then repeatedly calles that element until Selenium throws a 
StaleElementReferenceException, meaning the element is no longer attached to the page’s DOM and the site has 
redirected. Checks the page every half second, with a time-out of 10 seconds'''

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print('Connecting...')
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name('html')
        except StaleElementReferenceException:
            return

'''Initializes a url to be searched and a chrome browser using the path on the user's computer, and 
   then opens the url in the browser, waits for it to load, and creates a list of all elements with the tag <table>'''

url = "https://library.municode.com/oh/cincinnati/codes/code_of_ordinances?nodeId=TIXIZOCOCI_CH1409CODI_S1409-09DERE"
browser = webdriver.Chrome(executable_path='/Users/Jonah1/Downloads/chromedriver')
browser.get(url)
waitForLoad(browser)  # print(browser.page_source)
tables = browser.find_elements_by_tag_name("table")

keywords_to_look_for = ['far', 'floor area ratio', 'building', 'percent', 'height', 'area',
                        'maximum', 'minimum', 'feet', 'square', 'ft', 'parking', 'density', 'yard', 'total', 'number'
                        'gross', 'buildable', 'lot', 'coverage', 'ratio', 'residential', 'office', 'floor',
                        'front', 'primary', 'secondary', 'side', 'rear', 'setback', 'use', 'flr'
                        ]
# print(tables)

'''Loops through all of the tables on a page, storing the content/text of the table as the Key of a dictionary and a list of the
keywords from keywords_to_look_for that appeared in the text of the table as the value of the dictionary. Finds if any of the keywords
are in the text of a table by forming a giant string containing all of the text for each table in the loop and then loops through the
keywords_to_look_for list to see if the giant string contains the word or string of words, storing the words that are found, inside
of a list that will be used as the value of the dictionary. Also, keeps track of the number of tables found in the page/looped through
letting the person running the bot at the end of each cycle of the loop that the bot has finished scraping data for table number x'''

table_keyword_count = {}
table_count = 0
for table in tables:
    table_count += 1
    key_found_list = []
    table_text = ""
    rows = table.find_elements_by_tag_name("tr")  # get all of the rows in the table
    for row in rows:
        cells = row.find_elements_by_tag_name("td") # get all the cells in the row
        # note: index start from 0, 1 is the 2nd cell
        for cell in cells:
            table_text += cell.text  # adds the text from each cell to a string
    for keyword in keywords_to_look_for:    
        if keyword in table_text.lower():
            key_found_list.append(keyword)  # looks through all the text from the table and adds all keywords found to a list
    table_keyword_count[table] = key_found_list
        # print(key_found_list) # Testing
    print('Finished Searching Table #'+ str(table_count))

'''Sorts the dictionary in descending order using the length of the list of keywords, being the value of the dictionary. In other words,
sorts the tables so that the tables that contain the most number of keywords appear first to the user and the ones with the least appear
last. Sorts the list of tables using the sorted() method: the keys and values of the dictionary are inputted for the first argument,
being the sequence/list that will be looped through, in the second argument which decides how they will be ordered, lambda (an anonymous function/a small 
function that only has one expression) is used and in lambda the key of the dictionary is passed as "x" in the argument, in the third
argument we passed reverse=True to sort the tables in descending order based on the length of the list/amount of keywords found in the table's
contents. Note: doing name_of_key[0] gets the key of a dictionary and name_of_key[1] gets the value in a dictionary'''

sorted_tables = sorted(table_keyword_count.items(), key=lambda x: len(x[1]), reverse=True)
for table in sorted_tables:  # iterates through the dictionary
    print('\nAmount of Keywords: ' + (str(len(table[1]))) + ' | Keywords: ', end='') # prints the amount of keywords, and prints without creating a new line
    print(table[1], end='')
    print('\n')
    rows = table[0].find_elements_by_tag_name("tr")  # get all of the rows in the table, which is the key in the dictionary
    # Note: doing name_of_key[0] (being table[0]) gets the key of a dictionary and name_of_key[1] (being table[1]) gets the value in a dictionary
    for row in rows:
        cells = row.find_elements_by_tag_name("td")
        print(" | ".join([cell.text for cell in cells])) # print all the cells in the row
        print("--------")  
    print("***************************************************************************************")

browser.close     # Closes the browser
browser.quit()