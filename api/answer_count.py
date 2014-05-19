import unirest
import settings
import threading

SYNC_INTERVAL = 43200 # 43200 sec = 12 hrs
    
def get_all_questions():
    response = unirest.get(settings.API_URL + 'question/', headers={'Content-Type':'application/json'})
    questions = response.body['_items']
    return questions

def get_all_answers():
    response = unirest.get(settings.API_URL + 'answer/', headers={'Content-Type':'application/json'})
    answers = response.body['_items']
    return answers

def set_nAnswers(qid, nAnswers):
    response = unirest.get(settings.API_URL + 'question/' + qid, headers={'Content-Type':'application/json'})
    datum = {"answers": str(nAnswers)}
    etag = response.body['_etag']

    response2 = unirest.patch(settings.API_URL +
            'question/' + qid,
            headers={'Accept':'application/json', 'If-Match': etag}, params=datum)

def syncer():
    questions = get_all_questions()
    answers = get_all_answers()

    # for each question, determine how many answers it has, set this as attr
    for question in questions:
        numAnswers = 0
        for answer in answers:
            if answer['question'] == question['_id']:
                numAnswers += 1
        if numAnswers is not int(question['answers']):
            set_nAnswers(question['_id'], numAnswers)

def main():
    t = threading.Timer(SYNC_INTERVAL, syncer)
    t.start()

if __name__ == '__main__':
    main()
