import urllib.request as request
import json


def get_token(email, password):
    req = request.Request(
        "https://api.busuu.com/anon/login",
        json.dumps({
            "email": email,
            "password": password
        }).encode(),
        {
            "Content-Type": "application/json"
        }
    )
    str_result = ""
    with request.urlopen(req) as f:
        str_result = str_result + f.read().decode('utf-8')
    json_result = json.loads(str_result)
    if json_result['status'] == "ok":
        return json_result['data']['access_token']


def get_vocabulary(token):
    req = request.Request(
        "https://api.busuu.com/vocabulary/all/enc?translations=enc,zh&access_token=" + token
    )
    str_result = ""
    with request.urlopen(req) as f:
        str_result = str_result + f.read().decode('utf-8')
    result = json.loads(str_result)
    return result


def vocabulary_factory(raw):
    vocabularies = raw['vocabulary']
    entity_map = raw['entityMap']
    translation_map = raw['translationMap']
    for vocabulary in vocabularies:
        entity_id = vocabulary['entity_id']
        entity = entity_map[entity_id]
        phrase = entity['phrase']
        keyphrase = entity['keyphrase']
        image_url = entity['image']
        is_vocabulary = entity['vocabulary']

        phrase_content = translation_map[phrase]
        phrase_content_en = phrase_content.get('enc', {})
        f_phrase = phrase_content_en.get('value', '')
        f_phrase_audio = phrase_content_en.get('audio', '')
        phrase_content_zh = phrase_content.get('zh', {})
        f_phrase_cn = phrase_content_zh.get('value', '')

        example_content = translation_map[keyphrase]
        example_content_en = example_content.get('enc', {})
        f_example = example_content_en.get('value', '')
        f_example_audio = example_content_en.get('audio', '')
        example_content_zh = example_content.get('zh', {})
        f_example_cn = example_content_zh.get('value', '')

        yield entity_id, f_phrase, image_url, f_phrase_cn, f_phrase_audio, f_example, f_example_cn, f_example_audio


# for entity_id, phrase, image, meaning, audio, example, example_meaning, example_audio in vocabulary_factory(raw):
def fetch_vocabulary(username, password):
    token = get_token(username, password)
    raw = get_vocabulary(token)
    return vocabulary_factory(raw)
