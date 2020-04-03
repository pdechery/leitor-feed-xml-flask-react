# -*- coding: utf-8 -*-

from html.parser import HTMLParser

class parseItemContent(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        
        self.ps, self.imgs, self.uls = [], [], []
        self.getP, self.getUl, self.getImg = 0, 0, 0

        self.data = {
            'ps': self.ps,
            'imgs': self.imgs,
            'uls': self.uls
        }

    def handle_starttag(self, tag, attrs):
        if (tag == 'p'):
            self.ps.append('<p>')
            self.getP = 1
        elif(tag == 'img'):
            for attr in attrs:
                if(attr[0] == 'src'):
                    self.imgs.append(attr[1])
        elif(tag == 'li'):
            self.getUl = 1
        elif(tag == 'a'):
            if(self.getUl):
                self.uls.append(attrs[0][1])
        else:
            return

    def handle_endtag(self, tag):
        if (tag == 'p'):
            self.ps.append('</p>')
            self.getP = 0
        elif(tag == 'li'):
            self.getUl = 0
        else:
            return

    def handle_data(self, data):
        if(self.getP):
            nospace = data.strip()
            self.ps.append(nospace)
        else:
            return