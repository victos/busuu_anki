import json

from urllib import request
from urllib.request import Request

BASE_URL = 'https://od-api-demo.oxforddictionaries.com:443/api/v1'
QUERY_URL = '/entries/{0}/{1}/regions={2}'


def query(word, source_lang='en', region='us'):
    req = Request('%s%s' % (BASE_URL, QUERY_URL.format(source_lang, word, region)), headers={
        'Accept': 'application/json',
        'app_id': '5037d509',
        'app_key': '4dc1aebaa63721f0f8e79a55e2514bc7'
    })
    with request.urlopen(req) as f:
        print(f.read().decode('utf-8'))

if __name__ == '__main__':
    print(query('hello'))
