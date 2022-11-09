from selenium import webdriver
import pandas as pd

class Zoning_Score():
    def __init__(self, keyword_csv, element):
        self.keyword_csv = keyword_csv
        self.keywords = {}
        self.element = element

    def create_keyword_dict(self, keyword_csv):
        df = pd.read_csv(keyword_csv)
        dict = {}
        for col in df.columns:
            dict[col] = df[col].to_list()
        self.keywords = dict
        print(self.keywords)

    def get_zoning_boolean(self, element):
        for list in self.keywords.values():
            for keyword in list:
                if keyword.lower() in element.text.lower():
                    print("found it!", keyword)
                    return True
        return False

    def create_score_dict(self, element):
        score_dict = {}
        keywords = self.keywords
        print(keywords)
        for key, value in keywords.items():
            counter = 0
            for keyword in value:
                if keyword.lower() in element.text.lower():
                    counter += 1
            score_dict[key] = counter
        return score_dict

    def get_zoning_label(self, element):
        if self.get_zoning_boolean(element):
            return self.create_score_dict(element)
        print("No keywords in this element")
        return False

    def run_script(self):
        element = self.element
        keyword_csv = self.keyword_csv
        self.create_keyword_dict(keyword_csv)
        return self.get_zoning_label(element)


driver = webdriver.Chrome(executable_path='/Users/Jonah1/Downloads/chromedriver') # use path to chromedriver
url = "http://quotes.toscrape.com/page/2/"
driver.get(url)
element = driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[1]/span[1]')
print(element.text)

test = Zoning_Score(open("/Users/Jonah1/Downloads/keywords.csv"), element)  # use path to csv 
print(test.run_script())
driver.quit()

