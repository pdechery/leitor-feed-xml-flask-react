# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import requests
from requests.exceptions import HTTPError
import html
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
#from htmlparser import parseItemContent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def getContent():
    try:
            
        response = requests.get('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
        response.raise_for_status()

        parsedXml = ET.fromstring(response.content)
        
        items = parsedXml.findall('./channel/item')

        response = {'feed':[]}

        for item in items:
            
            nItem = {}

            ContentMarkup = item.find('description').text

            # parseando o HTML do conteúdo com biblioteca externa
            soup = BeautifulSoup(ContentMarkup, 'html.parser')

            for tag in soup.find_all(True):
                #print(type(tag))
                #print(tag.name)
                if(tag.name == 'p'):
                    #print(type(tag.string))
                    #print(tag.contents)
                    print(str(tag))
                elif(tag.name == 'img'):
                    if(tag.find_parent("div")):
                        print(tag['src'])
                elif(tag.name)
            
            # paragraphs = [str(p) for p in soup.find_all('p')]
            # images = [img['src'] for img in soup.select("div.foto > img")]
            # links = [link['href'] for link in soup.select("ul li > a")]

            paragraphs = ' '.join(paragraphs)

            description = []

            nItem['title'] = item.find('title').text
            nItem['link'] = item.find('link').text
            nItem['description'] = [
                {
                    'type': 'text',
                    'content' : paragraphs
                },
                {
                    'type': 'image',
                    'content' : images
                },
                {
                    'type': 'links',
                    'content': links
                }
            ]

            response['feed'].append({'item': nItem })

        return jsonify(response)
    
    except HTTPError as http_err:
        print('Cool Exception')
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print('Regular Exception')
        print(err)
 
if __name__ == '__main__':
    #app.run(debug=True, host='0.0.0.0')
    print(getContent())