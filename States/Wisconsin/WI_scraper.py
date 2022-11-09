from bs4 import BeautifulSoup
import requests

class Wisconsin_Bot():
    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.site = "https://www.wdfi.org/apps/CorpSearch/Results.aspx?type=Simple&q=" + entity_name

    def initialize_bs(self, site):
        bs = BeautifulSoup(requests.get(site).content, "html.parser")

        return bs
    # Combines multi-line strings into one one-line string
    def cleanData(self, data):
        split = data.split('\r\n')
        result = ""
        for string in split:
            result += string.strip() + " "
        return result.strip()

    # Navigates to the company specific page on the website
    def startSoupAndFindDetails(self, bs):
        firstResult = bs.find("td", {"class": "nameAndTypeDescription"})
        link = firstResult.find("a")
        detailsSite = "https://www.wdfi.org/apps/CorpSearch/" + link["href"]
        bs = BeautifulSoup(requests.get(detailsSite).content, "html.parser")
        return bs

    # Scrapes all general information about the company as well as information on specific agents
    def scrapeData(self, bs):
        fullDict = {
            'Information': {}
        }
        fullDict['Information']['Entity Name'] = self.cleanData(bs.find("h1", {"id": "entityName"}).text)
        keys = bs.find_all("td", {"class": "label"})
        values = bs.find_all("td", {"class": "data"})
        for i in range(9):
            fullDict['Information'][self.cleanData(keys[i].text)] = self.cleanData(values[i].text)

        if 'Registered Agent Office' in fullDict['Information'].keys():
            temp = fullDict['Information']['Registered Agent Office'].split()
            address_start = -3
            file_index = 0
            for i in range(len(temp)):
                if temp[i].isdigit() and address_start == -3:
                    address_start = i
                if temp[i] == 'File':
                    file_index = i
            agent_name = ' '.join(temp[:address_start]).strip()
            agent_address = ' '.join(temp[address_start: file_index]).strip()
            del fullDict['Information']['Registered Agent Office']
            agent = {
                'Name': agent_name,
                'Address': agent_address
            }
            fullDict['Agent'] = agent

        return fullDict

    def run_script(self):
        site = self.site
        bs = self.initialize_bs(site)
        detail_page = self.startSoupAndFindDetails(bs)

        return self.scrapeData(detail_page)
