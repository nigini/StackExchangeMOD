import stackexchange
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING, DESCENDING
import datetime
import html

now = datetime.datetime.now()
site = 'pt.stackoverflow.com'

db_client = MongoClient()
db = db_client[site.replace('.','_')]
db_tags = db.tags

ptso = stackexchange.Site(site)
tags = ptso.tags()

for tag in tags:
    try:
        name = html.unescape(tag.json['name'])
        tag.json['name'] = name
        tag.json.pop('_params_')
        tag.json['timestamp']=now

        db_tags.insert(tag.json)
        print('INSERTED: {}'.format(name))
    except DuplicateKeyError:
        print('ERROR - DUP: {}'.format(name))
    except KeyError:
        print('ERROR - KEY: {}'.format(name))

db_tags.create_index([('name',ASCENDING)])
db_tags.create_index([('count',DESCENDING)])