import io
import xml.etree.ElementTree as xml
from collections import Iterator

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


def get_pdf_pages(filepath: str):
    with open(filepath, 'rb') as f:
        for page in PDFPage.get_pages(f, caching=True, check_extractable=True):
            pdf_rm = PDFResourceManager()
            out_stream = io.StringIO()  # create in-memory text stream
            converter = TextConverter(pdf_rm, out_stream)
            pdf_pi = PDFPageInterpreter(pdf_rm, converter)
            pdf_pi.process_page(page)

            page_text = out_stream.getvalue()
            yield page_text

            # finalizer
            converter.close()
            out_stream.close()


def parse_pdf(filepath: str):
    root = xml.Element('root')
    for num, page in enumerate(get_pdf_pages(in_filename)):
        block = xml.SubElement(root, 'block')
        block.set("number", str(num))
        block.text = page
        block.tail = '\n'
    tree = xml.ElementTree(root)
    out = open(out_filename, 'w')
    tree.write(out, encoding='unicode', xml_declaration=True, method="xml")


in_filename = "../samples/sample.pdf"
out_filename = "../out/pdf_parsing_result.xml"
parse_pdf(in_filename)
