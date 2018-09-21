import json
import xml.etree.ElementTree
import dicttoxml
import re
import pandas as pd
import pudb
#pudb.set_trace()
def clean_building(element):
    '''
    removes floor information
    '''
    unwanted = ['中層','低層','高層']
    for item in unwanted:
        element = element.replace(item, '').strip()
    return element

def extract_digit(element):
    '''
    '''
    # element = (re.sub("[+().-]", "", element))
    # element = (re.sub("[A-Z a-z]", "", element))
    # element = element.lstrip().rstrip()
    element = re.findall(r'[0-9,.]+', element)
    if len(element)>0:
        element = re.sub(r"[$+(),-]", "", element[0])
    try:
        element = float(element)
    except:
        element = 0.0
    return element

#FILE = 'centanet.jl'
FILE = 'midland.jl'
_FILE = 'midland.csv'
_FILE_FINAL = 'midland_final.csv'
df_en = pd.read_json(FILE, lines=True)
df_en.to_csv(_FILE, encoding = 'utf-8')

df_en = pd.read_csv(_FILE, encoding='utf-8')
df_en['area'] = df_en['area'].apply(lambda x: extract_digit(x))
df_en['building_name'] = df_en['building_name'].apply(lambda x: clean_building(x))
df_en['price'] = df_en['price'].apply(lambda x: extract_digit(x))
df_en.to_csv(_FILE_FINAL, encoding="utf-8")
