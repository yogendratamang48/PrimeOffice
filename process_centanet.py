import json
import xml.etree.ElementTree
import dicttoxml
import re
import pandas as pd
import pudb
#pudb.set_trace()
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

FILE = 'centanet.jl'
df_en = pd.read_json(FILE, lines=True)
df_en['area'] = df_en['area'].apply(lambda x: extract_digit(x))
df_en['price'] = df_en['rent'].apply(lambda x: 1000000*extract_digit(x))
df_en.to_csv("centanet.csv", encoding="utf-8")
