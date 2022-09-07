import hashlib
import json
import requests
import time
import urllib.parse

from os.path import exists


def file_get_contents(filename):
    with open(filename, 'r', encoding='UTF-8') as f:
        s = f.read()
    return s


def file_put_contents(filename, content):
    with open(filename, 'w', encoding='UTF-8') as f:
        f.write(content)


def load_json_file(filename):
    return json.loads(file_get_contents(filename))


def fetch_url(url, cache=True):
    urlhash = hashlib.sha1(url.encode()).hexdigest()
    filepath = 'cache/{}.html'.format(urlhash)
    if cache and exists(filepath):
        return file_get_contents(filepath)
    response = requests.get(url, headers={'User-Agent': 'github.com/envlh/wmf-board-elections'}, allow_redirects=False)
    if response.status_code != 200:
        print('Failure while processing URL {} (HTTP code {}).'.format(url, response.status_code))
        exit(1)
    file_put_contents(filepath, response.text)
    time.sleep(5)
    return response.text


def fetch_url_json(url, cache=True):
    return json.loads(fetch_url(url, cache))


def sparql_query(query):
    url = 'https://query.wikidata.org/sparql?{}'.format(urllib.parse.urlencode({'query': query, 'format': 'json'}))
    return fetch_url_json(url, False)['results']['bindings']
