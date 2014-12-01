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

page=1 #These two should be received in "sys.argv"
max_page=1000000000 #Too large to be true
while(page<max_page):
    tags = ptso.tags(page=page,pagesize=100,sort='name',order='asc')
    if(len(tags)==0):
        break
    else:
        page+=1
        for i in range(len(tags)-1):
            try:
                tag=tags[i].json
                name = html.unescape(tag['name'])
                tag['name'] = name
                tag.pop('_params_')
                tag['timestamp']=now
                db_tags.insert(tag)
                print('INSERTED: {}'.format(name))
            except DuplicateKeyError:
                print('ERROR - DUP: {}'.format(name))
            except KeyError:
                print('ERROR - KEY: {}'.format(name))

db_tags.create_index([('name',ASCENDING)])
db_tags.create_index([('count',DESCENDING)])