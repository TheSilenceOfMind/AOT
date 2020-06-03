import xml.etree.ElementTree as xml

import requests
from bs4 import BeautifulSoup

in_url = "https://towardsdatascience.com/scraping-covid19-data-using-python-80120eb5eb66"
out_filename = "../out/html_parsing_result.xml"

rs = requests.get(in_url)
root = xml.Element('root')
if rs.status_code == 200:
    parsed_input = BeautifulSoup(rs.text, 'lxml')
    for tag in parsed_input.find_all("p"):  # choose and parse only <p>
        block = xml.SubElement(root, 'block')
        block.text = tag.text
        block.tail = '\n'
else:
    exit(-1)

tree = xml.ElementTree(root)
out_file = open(out_filename, 'w+')
tree.write(out_file, encoding='unicode', xml_declaration=True, method="xml")
