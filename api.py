import requests
import os
import subprocess
from urllib.parse import quote_plus

T411_URL = "http://api.t411.ai"
DOWNLOAD_DIR = 'downloaded'

class API:
    def __init__(self):
        self.token = None

    def auth(self, username, password):
        """Authenticate on T411 api, exits on error
        Change AUTH_TOKEN value to valid Authorization token
        Args:
            username(str): T411 username
            password(str): T411 password
        Returns: nothing
        """

        # Authenticating
        post_fields = {'username': username, 'password': password}

        r = requests.post(T411_URL + '/auth', post_fields)
        response = r.json()

        if 'error' in response:
            print(response['error'])
            raise SystemExit

        self.token = response['token']

    def persistent_auth(self):
        try:
            fp = open('token.txt', 'r')
            # Reading token from file
            self.token = fp.readline()
        except FileNotFoundError:
            self.auth(input("Nom d'utilisateur: "), input("Mot de passe: "))
            fp = open('token.txt', 'w')
            # Writing token to file
            fp.write(self.token)

    def query(self, path, params=None):
        r = requests.get(T411_URL + path, params,
                headers={'Authorization': self.token})

        return r

    def search(self, query, **kwargs):
        params = {
            'offset':0
        }
        params.update(kwargs)
        q = self.query('/torrents/search/%s' % query, params)
        response = q.json()

        #TODO eviter la répétition avec la gestion de l'erreur dans auth()
        if 'error' in response:
            print(response['error'])
            raise SystemExit
        return response

    def download(self, torrent):
        """Download a .torrent to disk
        :param torrent: a json torrent description
        """

        file_name = quote_plus(torrent['name']) + '.torrent'
        torrent_id = torrent['id']
        q = self.query('/torrents/download/%s' % torrent_id)

        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        with open("%s/%s" % (DOWNLOAD_DIR, file_name), 'wb') as  t_fic:
            t_fic.write(q.content)
            print('%s créé' % file_name)
        return "%s\%s\%s" % (os.getcwd(), DOWNLOAD_DIR, file_name)
