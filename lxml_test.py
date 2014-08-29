from lxml import etree


class _Element(etree.ElementBase):
    def __init__(self, *args, **kwargs):
        super(_Element, self).__init__(*args, **kwargs)

    @property
    def utf8_text(self):
        '''
        utf-8 wrapper property of lxml.etree.Element.text

        Note that this property has a same value with lxml.etree.Element.text
        internally but it returns utf-8 encoded string instead of unicode when
        getter called. It also allows both str and unicode format for an input.
        '''
        text = self.text
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        return text

    @utf8_text.setter
    def utf8_text(self, value):
        if isinstance(value, str):
            value = value.decode('utf-8')
        self.text = value


parser_lookup = etree.ElementDefaultClassLookup(element=_Element)
parser = etree.XMLParser()
parser.set_element_class_lookup(parser_lookup)

Element = parser.makeelement
SubElement = etree.SubElement

if __name__ == '__main__':
    elem = Element('Test')
    sub = SubElement(elem, 'FOO')
  
    sub.utf8_text = '\xef\xbc\xa1'
    print sub.text
    xml_string = etree.tostring(elem, xml_declaration=True, encoding='UTF-8')
    print xml_string
    elem = etree.fromstring(xml_string, parser)
    print elem.find('FOO').utf8_text
    print isinstance(elem, _Element)
