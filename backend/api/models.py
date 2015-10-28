from pymongo import MongoClient
from bson.json_util import dumps

class Tag():

    def __init__(self, site_name):
        db_client = MongoClient()
        db = db_client[site_name.replace('.','_')]
        self.db_tags = db.tags

    def get_all(self):
        query = {} 
        result = self.db_tags.find(query)
        to_return = []
        for r in result:
            to_return.append(self._format_result(r))
        return to_return

    def get_by_name(self, name):
        query = {'name':name} 
        result = self.db_tags.find_one(query)
        return self._format_result(result)

    def _format_result(self, result):
        if result:
            result.pop('_id')
            result.pop('timestamp')
            return dumps(result)
        else:
            return '{}'

