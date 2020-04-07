# -*- coding: utf-8 -*-

from flask import Flask, jsonify, json, request, Response, render_template, abort
import requests, html
from config import config
from requests.exceptions import HTTPError
from functools import wraps
import xml.etree.ElementTree as ET
from utils.htmlparser import parseItemContent
from utils.auth import Auth

app = Flask(__name__, template_folder='templates')
app.config['JSON_AS_ASCII'] = False

def auth_token_required(f):
    @wraps(f)
    def verify_token(*args, **kwargs):
        auth = Auth()
        try:
            result = auth.verify_auth_token(request.args.get('token'))
            if result['status'] == 200:
                return f(*args, **kwargs)
            else:
                abort(result['status'], result['message'])
        except KeyError as e:
            abort(401, 'Você precisa enviar um token de acesso')
            
    return verify_token


@app.route('/app/feed')
@auth_token_required
def get():
    try:     
        response = requests.get(config['feed_url'])
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


@app.route('/login', methods=['POST'])
def doLogin():
        
    if(request.form['username'] == config['username'] and request.form['password'] == config['password']):
        auth = Auth()
        data = {
            'username': config['username'],
            'senha': config['password']
        }
        response = {
            'access_token': auth.generate_auth_token(data).decode('utf-8'),
            'token_type': "JWT"
        }
        return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json'), 200
    else:
        abort(401, 'Dados não encontrados')


@app.route('/')
def getIndex():
    return render_template('index.html', data={})
 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')