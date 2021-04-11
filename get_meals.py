import requests

from xml.dom import minidom

parsed_sitemap = minidom.parseString(requests.get('https://allplants.com/sitemap.xml').text)

urls = parsed_sitemap.getElementsByTagName('loc')

for url_node in urls:
    url = url_node.firstChild.data
    
    if '/products/' in url:
        name = url.split('/')[-1]
        with open(f'uncommitted/{name}.html', 'w') as out:
            out.write(requests.get(url).text)
