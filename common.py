from urllib.parse import quote_plus

def most_seeded(torrents, *, num=None):
        """Returns max seeded torrent
        :param torrents: a list of dicts
        :return: a (dict) torrent or a list of dict with length = num
        """

        top = sorted(torrents, key=lambda x:int(x['seeders']), reverse=True)
        return (top[0] if num is None else top[0:num])

def choice(torrents):
    for i,torrent in enumerate(torrents):
        print("%d - %s (%s seeders)" % (i, torrent['name'], torrent['seeders']))
    num_choice = int(input('\nÉcrire le numéro du torrent choisi : '))
    return torrents[num_choice]

def ask_query():
    return quote_plus(input('Entrer une recherche: '))
