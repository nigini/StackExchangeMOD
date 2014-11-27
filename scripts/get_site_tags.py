import stackexchange
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING, DESCENDING
import datetime

now = datetime.datetime.now()
site = 'pt.stackoverflow.com'

db_client = MongoClient()
db = db_client[site.replace('.','_')]
db_tags = db.tags

ptso = stackexchange.Site(site)
tags = ptso.tags()

for tag in tags:
    try:
        tag.json.pop('_params_')
        tag.json['timestamp']=now
        db_tags.insert(tag.json)
        print('INSERTED: {}'.format(tag.json['name']))
    except DuplicateKeyError:
        print('ERROR - DUP: {}'.format(tag.json['name']))
    except KeyError:
        print('ERROR - KEY: {}'.format(tag.json['name']))

db_tags.create_index([('name',ASCENDING)])
db_tags.create_index([('count',DESCENDING)])