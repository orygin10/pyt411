from api import API
from common import *
import os

def main():
    api = API()
    api.persistent_auth()

    query = ask_query()

    s = api.search(query, limit=1000)
    torrents = s.get('torrents')

    dl = choice(most_seeded(torrents, num=10))

    tfile = api.download(dl)
    os.startfile(tfile)

if __name__ == '__main__':
    main()
