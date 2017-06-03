 # -*- encoding: utf8 -*-
import requests
import os
import subprocess
from urllib import pathname2url
import string

"""
@var T411_URL: T411 valid api URL
@var DOWNLOAD_DIR: Directory in which .torrents are downloaded
@ivar token: T411 API Authentication Token
"""

T411_URL = "http://api.t411.al"
DOWNLOAD_DIR = 'downloaded'

class RequestsError(Exception):
    """Error in API response"""
    pass

class AuthError(Exception):
    """Error while authenticating"""
    pass

class API:
    def __init__(self):
        self.token = None

    def auth(self, username, password):
        """
        @param username: valid t411 username
        @param password: valid plaintext t411 password
        @summary: retrieves an authentication token from t411 api
        @raise AuthError: Username or password invalid
        """

        # Authenticating
        post_fields = {'username': username, 'password': password}

        r = requests.post(T411_URL + '/auth', post_fields)
        response = r.json()

        if 'error' in response:
            raise AuthError(response['error'])

        self.token = response['token']

    def persistent_auth(self):
        """reads token from file or creates a new one
        then stores it in token instance variable
        @raise AuthError: Token verification failure
        """
        if os.path.exists('token.txt'):
            with open('token.txt', 'r') as fp:
                self.token = fp.readline()
        else:
            self.auth(raw_input("Nom d'utilisateur: "), raw_input("Mot de passe: "))
            with open('token.txt', 'w') as fp:
                # Writing token to file
                fp.write(self.token)

        q = self.query('/torrents/search/windows') # Testing auth token
        response = q.json()
        if 'error' in response:
            raise AuthError("Token is invalid")

    def query(self, path, params=None):
        """
        @summary: Webservice query on t411 api
        @param path: Full query plaintext path for exemple /torrents/download/45224
        @type path: str
        @param params: Optional params for query; offset or limit
        @type params: dict
        @return: JSON response
        @rtype: str
        """
        return requests.get(T411_URL + path, params,
                headers={'Authorization': self.token})

    def raw_search(self, query, **kwargs):
        """
        @summary: Search a torrent on t411
        @param query: Valid URL-Formatted torrent query for exemple "Windows%20Seven"
        @type query: str
        @return: Found torrents
        @rtype: Parsed JSON
        @raise RequestsError: Response can't be parsed to JSON
        """
        params = {
            'offset':0
        }
        params.update(kwargs)
        q = self.query('/torrents/search/%s' % query, params)
        response = q.json()

        if 'error' in response:
            raise RequestsError(response['error'])
        return response

    def raw_download(self, torrent):
        """
        @summary: Downloads torrent to disk
        @param torrent: Torrent to download
        @type torrent: dictionary
        @return: Path of the downloaded torrent
        @rtype: str
        """
        def format_filename(s):
            """
            @summary: Replace ambiguous filename chars with standard chars
            @param s: Raw filename
            @type s: str
            @return: Formatted filename
            @rtype: str
            """
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            filename = ''.join(c for c in s if c in valid_chars)
            filename = filename.replace(' ', '_')  # I don't like spaces in filenames.
            return filename

        file_name = format_filename(torrent['name'] + '.torrent')
        torrent_id = torrent['id']
        q = self.query('/torrents/download/%s' % torrent_id)

        if not os.path.exists(DOWNLOAD_DIR):
            os.makedirs(DOWNLOAD_DIR)

        with open("%s/%s" % (DOWNLOAD_DIR, file_name), 'wb') as  t_fic:
            t_fic.write(q.content)
        return "%s\%s\%s" % (os.getcwd(), DOWNLOAD_DIR, file_name)
