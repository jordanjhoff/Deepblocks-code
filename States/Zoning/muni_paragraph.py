'''This program finds all the paragraph text on a page and then prints the paragraphs that have keywords present in it.
   The paragraphs are printed in descending order, with the paragraph with the most keywords in it printed first, and for each paragraph, 
   the amount of keywords present along with the keywords that are present within the paragraph are printed with the paragrpah itself.'''

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

'''Initalizes the url you are searching through and initializes a chrome browser using the path on the user's computer and
   then opens the url in the browser, waits for it to load, and creates a list of all elements with the tag <p>'''
          
url = "https://library.municode.com/va/henrico_county/codes/code_of_ordinances?nodeId=CD_ORD_CH24ZO_ARTVOMIREDIUS_S24-11PRUSPE"
browser = webdriver.Chrome(executable_path='/Users/Jonah1/Downloads/chromedriver')
browser.get(url)
waitForLoad(browser)  # print(browser.page_source) # Testing
text = browser.find_elements_by_tag_name("p")
keywords = {}

keywords_to_look_for = ['far', 'floor area ratio', 'building', 'percent', 'height', 'area',
                        'maximum', 'minimum', 'feet', 'square', 'ft', 'parking', 'density', 'yard', 'total', 'number'
                        'gross', 'buildable', 'lot', 'coverage', 'ratio', 'residential', 'office', 'floor',
                        'front', 'primary', 'secondary', 'side', 'rear', 'setback', 'use', 'flr'
                        ]

# 'far', 'floor area ratio', 'maximum building height', 'percent', 'maximum height',
# 'maximum', 'minimum', 'feet', 'square feet', 'sq ft', 'ft', 'parking', 'density', 'yard',
# 'setback', ' use', 'lot coverage ratio', 'flr', 'parking spots', 'parking ratio',
# 'total allowable area', 'total allowable square feet', 'total number of', 'number of',
# 'gross buildable', 'lot coverage', 'ratio', 'number of floors', 'residential', 'office',
# 'front setback', 'primary setback', 'secondary setback', 'side setback', 'rear setback'

'''Loops through all of the paragraphs on a page, storing the text of the paragraph as the Key of a dictionary and a list of the
keywords from keywords_to_look_for that appeared in the text of the paragraph as the value of the dictionary. Finds if any of the keywords
are in the paragraph by looping through the keywords_to_look_for list to see if the paragraph contains any of the keywords, storing the words 
that are found inside of a list that will be used as the value of the dictionary. If there are no keywords present in a paragraph, the paragraph
is not saved to the dictionary. '''

para_keyword_count = {}
for t in text:
    key_found_list = []
    for keyword in keywords_to_look_for:
        if keyword in t.text.lower():
            key_found_list.append(keyword) # looks through the paragraph and adds any keywords found to a list
    # print(key_found_list) Testing
    if key_found_list:  # only saves a paragraph if there are keywords present
        para_keyword_count[t.text] = key_found_list  

# print(para_keyword_count)

'''Sorts the dictionary in descending order using the length of the list of keywords, being the value of the dictionary. In other words,
sorts the paragraphs so that the paragraphs that contain the most number of keywords appear first to the user and the ones with the least appear
last. Sorts the list of paragraphs using the sorted() method: the keys and values of the dictionary are inputted for the first argument,
being the sequence/list that will be looped through, in the second argument which decides how they will be ordered, lambda (an anonymous function/a small 
function that only has one expression) is used and in lambda the key of the dictionary is passed as "x" in the argument, in the third
argument we passed reverse=True to sort the paragraphs in descending order based on the length of the list/amount of keywords found in the paragraph's
text. Note: doing name_of_key[0] gets the key of a dictionary and name_of_key[1] gets the value in a dictionary'''

sorted_para = sorted(para_keyword_count.items(), key=lambda x: len(x[1]), reverse=True)
for p in sorted_para: # iterates through the dictionary
    print('\n')
    print('Amount of Keywords: ' + (str(len(p[1]))) + ' | Keywords: ', end='') # prints the amount of keywords, and prints without creating a new line
    print(p[1]) # prints list of keywords
    print(p[0]) # prints the paragraph
    # Note: doing name_of_key[0] (being p[0]) gets the key of a dictionary and name_of_key[1] (being p[1]) gets the value in a dictionary

browser.close  # Closes the browser
browser.quit()
