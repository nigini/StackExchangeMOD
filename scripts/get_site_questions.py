import stackexchange
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo import ASCENDING, DESCENDING
import datetime

now = datetime.datetime.now()
site = 'pt.stackoverflow.com'

db_client = MongoClient()
db = db_client[site.replace('.','_')]
db_questions = db.questions

ptso = stackexchange.Site(site)

page=1 #These two should be received in "sys.argv"
max_page=1000000000 #Too large to be true
while(page<max_page):
    #ToDo: pagesize=100? and "no_answers"!?
    questions = ptso.questions(page=page,sort='creation',order='asc')
    if(len(questions)==0):
        break
    else:
        page+=1
        for i in range(len(questions)-1):
            try:
                question = questions[i].json
                question.pop('_params_')
                question['timestamp']=now
                db_questions.insert(question)
                print('INSERTED: {}'.format(question['question_id']))
            except DuplicateKeyError:
                print('ERROR - DUP: {}'.format(question['question_id']))
            except KeyError:
                print('ERROR - KEY: {}'.format(question['question_id']))

db_questions.create_index([('answer_count',ASCENDING)])
db_questions.create_index([('question_id',ASCENDING)])