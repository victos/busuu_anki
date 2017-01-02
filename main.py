import busuu.utils as utils

from anki.storage import Collection
from anki.notes import Note
from busuu.config import Busuu

conf = Busuu()


class AnkiBridge:
    def __init__(self, collection):
        self.collection = collection

    def add_busuu_entity_as_note(self, deck_name, model_name, busuu_entity, entity_mapping={
        'phrase': 'parase',
        'image': 'image',
        'meaning': 'meaning',
        'phrase_audio': 'phrase_audio',
        'example': 'example',
        'example_meaning': 'example_meaning',
        'example_audio': 'example_audio'
    }, tags=[]):
        if busuu_entity is None:
            return
        fields = {}
        for name, value in entity_mapping.items:
            fields[value] = busuu_entity[name]

        self.save_media(busuu_entity.image, fields, entity_mapping['image'], '<img src="{}" />')
        self.save_media(busuu_entity.phrase_audio, fields, entity_mapping['phrase_audio'], '[sound:{}]')
        self.save_media(busuu_entity.example_audio, fields, entity_mapping['example_audio'], '[sound:{}]')
        self.add_note(deck_name, model_name, fields, tags)

    def save_media(self, busuu_media, fields, key, template):
        if busuu_media is not None:
            name = busuu_media.name
            data = busuu_media.data
            fields[key] = template.format(name)
            if name is not None and data is not None:
                self.media().writeData(name, data)

    def add_note(self, deck_name, model_name, fields, tags):
        collection = self.collection()
        if collection is None:
            return

        note = self.createNote(deck_name, model_name, fields, tags)
        if note is None:
            return

        collection.addNote(note)
        collection.autosave()
        return note.id

    def can_add_note(self, dock_name, model_name, fields):
        return bool(self.createNote(dock_name, model_name, fields))

    def create_note(self, deck_name, model_name, fields, tags=[]):
        collection = self.collection()
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

        if not note.dupeOrEmpty():
            return note

    def collection(self):
        return self.collection

    def media(self):
        collection = self.collection()
        if collection is not None:
            return collection.media

    def model_names(self):
        collection = self.collection()
        if collection is not None:
            return collection.models.allNames()

    def model_field_names(self, model_name):
        collection = self.collection()
        if collection is None:
            return

        model = collection.models.byName(model_name)
        if model is not None:
            return [field['name'] for field in model['flds']]

    def deck_names(self):
        collection = self.collection()
        if collection is not None:
            return collection.decks.allNames()


def fetch_from_busuu():
    return utils.fetch_vocabulary(conf.get_username(), conf.get_password())


def get_collection():
    return Collection(conf.get_anki_db())


if __name__ == '__main__':
    col = get_collection()
    print(col.name())
    i = 1
    for entity in fetch_from_busuu():
        print("%d\t%s" % (i, entity.id))
        i += 1
