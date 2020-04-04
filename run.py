# -*- coding: utf-8 -*-

from flask import Flask, jsonify
import requests
from requests.exceptions import HTTPError
import html
import xml.etree.ElementTree as ET
from htmlparser import parseItemContent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/app/feed')
def get():
    try:
            
        response = requests.get('https://revistaautoesporte.globo.com/rss/ultimas/feed.xml')
        response.raise_for_status()

        parsedXml = ET.fromstring(response.content)
        items = parsedXml.findall('./channel/item')

        response = {'feed':[]}

        for item in items:
            
            nItem = {}

            ContentMarkup = item.find('description').text
            parser = parseItemContent()
            parser.feed(html.unescape(ContentMarkup))

            nItem['description'] = parser.content
            nItem['link'] = item.find('link').text
            nItem['title'] = item.find('title').text

            response['feed'].append({'item': nItem })

        return jsonify(response)
    
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(err)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')