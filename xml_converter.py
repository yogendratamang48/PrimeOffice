import json
import xml.etree.ElementTree
import dicttoxml
import re
import pandas as pd
# import pudb
# pudb.set_trace()

def extract_digit(element):
    '''
    '''
    # element = (re.sub("[+().-]", "", element))
    # element = (re.sub("[A-Z a-z]", "", element))
    # element = element.lstrip().rstrip()

    try:
        element = int(re.sub("\D", "", element))
    except:
        element = 0
    return element

keep =['building_name','location', 'area', 'rent']
df = pd.read_json('primeoffice_chinease.jl', lines=True)
df2 = df[keep]
df2['rent'] = df2['rent'].apply(lambda x: extract_digit(x.split('HK$')[-1]))
df2['area'] = df2['area'].apply(lambda x: extract_digit(x))

df2.to_json("primeoffice_chinese_filtered.jl", orient="records", lines=True)
df2.to_excel("primeOffice.xlsx", encoding="utf-8")

data = []

with open('primeoffice_chinese_filtered.jl') as f:
    for line in f:
        data.append(json.loads(line))

xml = dicttoxml.dicttoxml(data)
open("output_chi.xml", "wb").write(xml)
