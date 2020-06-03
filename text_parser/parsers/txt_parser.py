import xml.etree.ElementTree as xml

in_filename = "../samples/example.txt"
out_filename = "../out/txt_parsing_result.xml"

with open(in_filename) as fin:
    root = xml.Element('root')
    for line in fin:
        line = line.rstrip()  # too ease : just using separation by line feeds
        if line:  # just cutting the empty string, whatever. Looks much more nice
            block = xml.SubElement(root, "block")
            block.text = line
            block.tail = '\n'

tree = xml.ElementTree(root)
out_file = open(out_filename, 'w+')
tree.write(out_file, encoding='unicode', xml_declaration=True, method="xml")
