import unirest
import settings
from pprint import pprint

def get_all_questions():
    response = unirest.get(settings.API_URL + 'question/', headers={'Content-Type':'application/json'})
    questions = response.body['_items']
    return questions

def get_all_answers():
    response = unirest.get(settings.API_URL + 'answer/', headers={'Content-Type':'application/json'})
    answers = response.body['_items']
    return answers

def main():
    # response = unirest.get(settings.API_URL + '/post/536c3df3dae5f13314f7bb65', headers={'Content-Type':'application/json'})
    # pprint(response.body)

    # datum = {"views": "22"}
    # etag = response.body['_etag']

    # response2 = unirest.patch(settings.API_URL +
    #         '/post/536c3df3dae5f13314f7bb65',
    #         headers={'Accept':'application/json', 'If-Match': etag}, params=datum)
    # pprint(response2.body)



    questions = get_all_questions()
    answers = get_all_answers()
    # for each question, determine how many answers it has, set this as attr
    for question in questions:
        numAnswers = 0
        for answer in answers:
            if answer['question'] == question['_id']:
                numAnswers += 1
        #if numAnswers is not 


if __name__ == '__main__':
    main()
