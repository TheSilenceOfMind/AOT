from text_parser.parsers.docx_parser import *

if __name__ == '__main__':
    in_filename = 'samples/sample.docx'
    out = open("out/docx_parsing_result.xml", "bw")
    out.write(get_docx_text_in_xml(in_filename))
    out.close()
