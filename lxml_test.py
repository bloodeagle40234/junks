from lxml import etree


class _Element(etree.ElementBase):
    def __init__(self, *args, **kwargs):
        super(_Element, self).__init__(*args, **kwargs)

    @property
    def text(self):
        '''
        utf-8 wrapper property of lxml.etree.Element.text
        '''

        text = etree.ElementBase.text.__get__(self)
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        return text

    @text.setter
    def text(self, value):
        if isinstance(value, str):
            value = value.decode('utf-8')
        #setattr(etree.ElementBase, 'text', value)
        #etree._Element.text.__set__(self, value)
        etree.ElementBase.text.__set__(self, value)


parser_lookup = etree.ElementDefaultClassLookup(element=_Element)
parser = etree.XMLParser()
parser.set_element_class_lookup(parser_lookup)

Element = parser.makeelement
SubElement = etree.SubElement

if __name__ == '__main__':
    elem = Element('Test')
    sub = SubElement(elem, 'FOO')
  
    sub.text = '\xef\xbc\xa1'
    print sub.text
    print type(sub.text)
    xml_string = etree.tostring(elem, xml_declaration=True, encoding='UTF-8')
    print xml_string
    elem = etree.fromstring(xml_string, parser)
    print elem.find('FOO').text
    print isinstance(elem, _Element)
