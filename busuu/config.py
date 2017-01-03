import json
import os


class Busuu:
    def __init__(self):
        with open("config.json") as config_file:
            config = json.load(config_file)
            self.username = config['username']
            self.password = config['password']
            self.anki_home = config['anki_home']
            self.profile = config['profile']

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_anki_db(self):
        return self.anki_home + self.profile + '/collection.anki2'
