from anki.storage import Collection
import busuu.utils as utils

from busuu.config import Busuu


conf = Busuu()


def fetch_from_busuu():
    return utils.fetch_vocabulary(conf.get_username(), conf.get_password())


def get_collection():
    print(conf.get_anki_db())
    return Collection(conf.get_anki_db())


if __name__ == '__main__':
    col = get_collection()
    print(col.name())
