 # -*- encoding: utf8 -*-
from urllib import pathname2url

def most_seeded(torrents, num=None):
        """Returns max seeded torrent
        :param torrents: a list of dicts
        :return: a (dict) torrent or a list of dict with length = num
        """

        top = sorted(torrents, key=lambda x:int(x['seeders']), reverse=True)
        return (top[0] if num is None else top[0:num])

def choice(torrents):
    for i,torrent in enumerate(torrents):
        print("%d - %s (%s seeders)" % (i, torrent['name'], torrent['seeders']))
    num_choice = int(input('\nTorrent choisi : '))
    return torrents[num_choice]

def ask_query():
    return pathname2url(raw_input('Entrer une recherche: '))
