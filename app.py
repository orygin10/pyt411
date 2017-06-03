 # -*- encoding: utf8 -*-
from api import API
from common import Common, choice, most_seeded
import os

def main():
    api = API()
    api.persistent_auth()

    c = Common(api)
    quit = False
    while not quit:
        query = raw_input("Recherche (q: arreter, s: mode saison) : ")
        if query == 's':
            c.download_season(raw_input("Saisissez la saison : "))
        elif query ==  'q':
            print 'Bye'
            quit = True
        else:
            torrents = c.search(query)
            chosen = choice(most_seeded(torrents, num=10))
            c.download(chosen)

if __name__ == '__main__':
    main()
