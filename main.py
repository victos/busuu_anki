import busuu.utils as utils
import json

from anki.storage import Collection
from anki.notes import Note
from busuu import config
from busuu.utils import BusuuMedia

conf = config.get_config()


class AnkiBridge:
    def __init__(self):
        self.collection = Collection(conf.get_anki_db())

    def add_busuu_entity_as_note(self, deck_name, model_name, busuu_entity, entity_mapping={
        'id': 'id',
        'phrase': 'phrase',
        'image': 'image',
        'meaning': 'meaning',
        'phrase_audio': 'phrase_audio',
        'example': 'example',
        'example_meaning': 'example_meaning',
        'example_audio': 'example_audio',
        'add_reverse': 'add_reverse'
    }, tags=['busuu'], add_reverse=True):
        if busuu_entity is None:
            return
        fields = {}
        for name, value in entity_mapping.items():
            if not isinstance(busuu_entity[name], BusuuMedia):
                fields[value] = busuu_entity[name]
        if entity_mapping['add_reverse'] is not None:
            if not add_reverse:
                fields[entity_mapping['add_reverse']] = None
            else:
                fields[entity_mapping['add_reverse']] = 'true'
        if self.can_add_note(deck_name, model_name, fields):
            self.save_media(busuu_entity.image, fields, entity_mapping['image'], '<img src="{}" />')
            self.save_media(busuu_entity.phrase_audio, fields, entity_mapping['phrase_audio'], '[sound:{}]')
            self.save_media(busuu_entity.example_audio, fields, entity_mapping['example_audio'], '[sound:{}]')
            return self.add_note(deck_name, model_name, fields, tags)
        else:
            return None, fields

    def save_media(self, busuu_media, fields, key, template):
        if busuu_media is not None:
            name = busuu_media.name
            data = busuu_media.data
            fields[key] = template.format(name)
            if name is not None and data is not None:
                self.media().writeData(name, data)

    def add_note(self, deck_name, model_name, fields, tags):
        collection = self.collection
        if collection is None:
            return None, fields

        note = self.create_note(deck_name, model_name, fields, tags)
        if note is None:
            return None, fields

        collection.addNote(note)
        collection.autosave()
        return note.id, fields

    def can_add_note(self, dock_name, model_name, fields):
        return bool(self.create_note(dock_name, model_name, fields))

    def create_note(self, deck_name, model_name, fields, tags=[]):
        collection = self.collection
        if collection is None:
            return

        model = collection.models.byName(model_name)
        if model is None:
            return

        deck = collection.decks.byName(deck_name)
        if deck is None:
            return

        note = Note(collection, model)
        note.model()['did'] = deck['id']
        note.tags = tags

        for name, value in fields.items():
            if name in note:
                note[name] = value
        # ignore duplicate item
        if not note.dupeOrEmpty():
            return note

    def media(self):
        collection = self.collection
        if collection is not None:
            return collection.media

    def model_names(self):
        collection = self.collection
        if collection is not None:
            return collection.models.allNames()

    def model_field_names(self, model_name):
        collection = self.collection
        if collection is None:
            return

        model = collection.models.byName(model_name)
        if model is not None:
            return [field['name'] for field in model['flds']]

    def deck_names(self):
        collection = self.collection
        if collection is not None:
            return collection.decks.allNames()

    def close_collection(self):
        self.collection.close()


def fetch_from_busuu():
    return utils.fetch_vocabulary(conf.get_username(), conf.get_password())


if __name__ == '__main__':
    bridge = AnkiBridge()
    for entity in fetch_from_busuu():
        # id, fields = bridge.add_busuu_entity_as_note("English", "English-Card", entity)

        entity_id, fields = bridge.add_busuu_entity_as_note("English", "busuu", entity,
                                                            entity_mapping={
                                                                'id': 'id',
                                                                'phrase': 'phrase',
                                                                'image': 'phrase_image',
                                                                'meaning': 'phrase_meaning',
                                                                'phrase_audio': 'phrase_audio',
                                                                'example': 'example',
                                                                'example_meaning': 'example_meaning',
                                                                'example_audio': 'example_audio',
                                                                'add_reverse': 'Add Reverse'
                                                            })
        print(entity_id, json.dumps(fields))
    bridge.close_collection()
