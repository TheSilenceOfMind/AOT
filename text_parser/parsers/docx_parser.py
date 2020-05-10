from xml.etree.ElementTree import XML
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import zipfile

"""
Module that extract text from MS XML Word document (.docx).
(Inspired by python-docx <https://github.com/mikemaccana/python-docx> and 
https://gist.github.com/etienned/7539105)
"""

WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
PARA = WORD_NAMESPACE + 'p'
TEXT = WORD_NAMESPACE + 't'
STYLE = WORD_NAMESPACE + 'pStyle'

STYLES_PRIORITIZED = {
    'Title': 0,
    'Heading1': 1,
    'Heading2': 2,
    'Heading3': 3,
    'Heading4': 4,
    'Normal': 5
}

DOC_TAG = 'doc'
BLOCK_TAG = 'block'


def get_docx_text_in_xml(path):
    """
    Take the path of a docx file as argument, return the parsed XML in unicode.
    See the structure in readme.md
    """
    global block
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = XML(xml_content)

    root = ET.Element(DOC_TAG)
    cur_tag = root
    for paragraph in tree.iter(PARA):

        # get style of paragraph
        p_num = -1
        for style_tag in paragraph.iter(STYLE):
            style = list(style_tag.attrib.values())[0]
            p_num = STYLES_PRIORITIZED.get(style)  # priority number

        # get text
        texts = [node.text
                 for node in paragraph.iter(TEXT)
                 if node.text]
        if not texts:
            continue

        # implement this feature
        # we have 3 cases : style is more than previous, less and equal;
        # if it is less ('higher') than stop forming current block, append to previous;
        # if it is equal than just append the paragraph;
        # if it is more ('less important style') than create new child and work with it;
        if p_num < 5:
            block = ET.SubElement(root, BLOCK_TAG)
            block.set('style', style)
            block.text = str(texts[0])
        else:
            text_block = ET.SubElement(block, BLOCK_TAG)
            text_block.set('style', style)
            text_block.text = str(texts[0])
    # ET.dump(root)  # for debug only
    return ET.tostring(root)
