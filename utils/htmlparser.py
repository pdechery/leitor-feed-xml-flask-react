# -*- coding: utf-8 -*-

from html.parser import HTMLParser

class parseItemContent(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        
        self.getData, self.isUl, self.isDiv = False, False, False
        self.paragraph, self.links, self.content = [], [], []

    def handle_starttag(self, tag, attrs):
        if (tag == 'p'):
            self.getData = True
        elif(tag == 'div'):
            self.isDiv = True
        elif(tag == 'img' and self.isDiv):
            for attr in attrs:
                if(attr[0] == 'src'):
                    self.content.append({
                        'type': 'image',
                        'content': attr[1]
                    })
        elif(tag == 'ul'):
            self.isUl = True
        elif(tag == 'a' and self.isUl):
            self.links.append(attrs[0][1])
        else:
            return

    def handle_endtag(self, tag):
        if (tag == 'p'):
            self.getData = False
            text = ' '.join(self.paragraph)
            if(text):
                text = text.replace(" ,", ",")
                self.content.append({
                    'type':'text',
                    'content': text
                })
            self.paragraph = []
        elif(tag == 'ul'):
            self.isUl = False
            self.content.append({
                'type':'links',
                'content': self.links
            })
        elif(tag == 'div'):
            self.isDiv = False
        else:
            return

    def handle_data(self, data):
        if(self.getData):
            nospace = data.strip()
            if(nospace):
                self.paragraph.append(nospace)
        else:
            return