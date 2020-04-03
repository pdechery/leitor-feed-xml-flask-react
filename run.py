# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import requests
from requests.exceptions import HTTPError
import xml.etree.ElementTree as ET
import html
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

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def get():
    try:
            
        response = requests.get('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
        response.raise_for_status()

        parsedXml = ET.fromstring(response.content)
        
        items = parsedXml.findall('./channel/item')

        feed = []
        dictFinal = {}

        for item in items:
            
            newItem = {}

            txtBase = item.find('description').text

            parser = parseItemContent()
            parser.feed(html.unescape(txtBase))
            
            clearString = ' '.join(parser.data['ps'])
            parser.data.update({'ps' : clearString})

            newItem['title'] = item.find('title').text
            newItem['description'] = parser.data
            newItem['link'] = item.find('link').text

            feed.append({'item': newItem })
            
        dictFinal['feed'] = feed

        return jsonify(dictFinal)
    
    except HTTPError as http_err:
        print('Cool Exception')
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print('Regular Exception')
        print(err)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')