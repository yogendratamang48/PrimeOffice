import json
import xml.etree.ElementTree
import dicttoxml
import pudb
pudb.set_trace()

keep =['building_name','location', 'area', 'rent', 'reference']
data = []
with open('primeoffice.jl') as f:
    for line in f:
        data.append(json.loads(line))

xml = dicttoxml.dicttoxml(data)
open("ouput.xml", "wb").write(xml)
