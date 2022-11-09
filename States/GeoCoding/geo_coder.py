import censusgeocode as cg
import pandas as pd
import time
import sys

# a longitude, latitude, and address are passed in and a dictionary with all of the census data is returned
def make_dict(x, y, address = 'No Address Inputted'):
    census = cg.CensusGeocode(benchmark='Public_AR_Census2010', vintage='Census2010_Census2010')
    limit = time.time() + 15

    # keeps trying to get the dictionary for 15 seconds, and if it doesn't work it stops the program and tells you what address was the problem
    while(True):
        if time.time() > limit:
            print("Could Not Find Census Data From: ", address)
            print('Timed Out After 15 Seconds')
            sys.exit()
        try:
            result_dict = census.coordinates(x=x, y=y)
            return result_dict
        except Exception:
            pass

# the input is a row of the dataframe, and the function gets the dictionary and makes a tuple of the GEOID,
# COUNTY, TRACT, and BLOCK.
def get_tuple(row):
    dict = make_dict(row.loc['Longitude'], row.loc['Latitude'], row.loc['UnparsedAddress'])
    tupled = (dict['States'][0]['GEOID'], dict['Counties'][0]['COUNTY'], dict['Census Tracts'][0]['TRACT'],
                dict['Census Blocks'][0]['BLOCK'])
    return tupled


# iterates through all rows of csv and creates a list "tuples" 
csv_path = "/Users/Jonah1/Downloads/Residential Sale Data.csv"
addresses = pd.read_csv(open(csv_path))
tuples = []
for i in range(len(addresses.index)):
    tuples.append(get_tuple(addresses.iloc[i]))



