# -*- encoding: utf8 -*-
from urllib import pathname2url
import os

class Common:

    def __init__(self, api):
        self.api = api

    def search(self, query):
        """
        @summary: search for torrents
        @param query: t411 query for exemple "Windows 10"
        @type query: str
        @rtype: List of dictionaries
         """
        query = pathname2url(query) + "*"
        s = self.api.raw_search(query, limit=1000)
        return s.get('torrents')

    def download(self, torrent):
        """
        @summary: Download a single torrent
        @param torrent: A single torrent
        @type torrent: dictionary
        """
        print "Downloading %s" % torrent['name']
        tfile = self.api.raw_download(torrent)
        os.startfile(tfile)

    def download_season(self, season_search_string, quality='1080p'):
        """
        @summary: Downloads full season
        @param season_search_string: Search string for exemple "Vikings s03"
        @type season_search_string: str
        """
        print '0 - VOSTFR (par defaut)\n1 - FRENCH'
        lang = 'FRENCH' if raw_input('Saisir 0 ou 1 : ') == 1 else 'VOSTFR'

        ep = 1
        fin_saison = False
        while not fin_saison:
            query = '%se%.2d* %s* %s' % (season_search_string,
                                          ep, quality, lang)
            torrents = self.search(query)

            if torrents == []:
                if quality == '1080p':
                    quality = '720p'
                elif quality == '720p':
                    print 'Fin de la saison'
                    fin_saison = True
            else:
                dl = most_seeded(torrents)
                self.download(dl)
                ep = ep + 1
                quality = '1080p'


def most_seeded(torrents, num=1):
    """Returns max seeded torrent
    @param torrents: Result of a search function
    @type torrents: List of dictionaries
    @return: Top [num] most seeded torrents
    @rtype: List of dictionaries
    """

    top = sorted(torrents, key=lambda x: int(x['seeders']), reverse=True)
    return top[0] if num == 1 else top[0:num]


def choice(torrents):
    """
    @param torrents: Ordered torrents
    @type torrents: A list of dictionaries
    @returns: One chosen torrent
    @rtype: Dictionary
    """
    for i, torrent in enumerate(torrents):
        print("%d - %s (%s seeders)" %
              (i, torrent['name'], torrent['seeders']))
    num_choice = int(input('\nTorrent choisi : '))
    return torrents[num_choice]