from lxml import html


def fetch_dict(CONFIG, item, _node):
    '''
    extracts dict data from single row
 ll   '''
    _selector = html.fromstring(_node)
    for key,value in CONFIG['fields'].items():
       for x in value:
           x_val = _selector.xpath(x)
           if len(x_val)>0:
               if key == 'floors_views':
                   item[key] = ', '.join(x_val)
                   break
               item[key] = x_val[0].strip()
               break
           else:
               item[key] = None
    return item
