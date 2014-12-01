from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING, DESCENDING
import datetime
from itertools import combinations

now = datetime.datetime.now()
site = 'pt.stackoverflow.com'

db_client = MongoClient()
db = db_client[site.replace('.','_')]
db_questions = db.questions
db_tags = db.tags


db_tags.update({},{'$set':{'q_answered':0,'t_relations':[]}},multi=True)

for question in db_questions.find():
    tags = question['tags']
    if len(tags)>1:
        for two_tags in combinations(tags,2):
            print('UPDATE:{} - {}'.format(question['question_id'],two_tags))
            #Trying not to hit DB more then once! =\
            op_0={}
            op_1={}
            if 'accepted_answer_id' in question.keys():
                op_0['$inc']={'q_answered':1}
                op_1['$inc']={'q_answered':1}
            if not db_tags.find_one({'name':two_tags[0],'t_relations.tag':two_tags[1]}):
                op_0['$addToSet']={'t_relations':{'tag':two_tags[1],'q_count':1}}
                op_1['$addToSet']={'t_relations':{'tag':two_tags[0],'q_count':1}}
                db_tags.update({'name':two_tags[0]},op_0)
                db_tags.update({'name':two_tags[1]},op_1)
            else:
                if('$inc' in op_0.keys()):
                    op_0['$inc']['t_relations.$.q_count']=1
                    op_1['$inc']['t_relations.$.q_count']=1
                else:
                    op_0['$inc']={'t_relations.$.q_count':1}
                    op_1['$inc']={'t_relations.$.q_count':1}
                db_tags.update({'name':two_tags[0],'t_relations.tag':two_tags[1]},op_0)
                db_tags.update({'name':two_tags[1],'t_relations.tag':two_tags[0]},op_1)
