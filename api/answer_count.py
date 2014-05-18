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
    #questions = get_all_questions()
    #answers = get_all_answers()

    # for each question, determine how many answers it has, set this as attr


if __name__ == '__main__':
    main()
