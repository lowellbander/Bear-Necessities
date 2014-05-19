import unirest
import settings

def main():
    qid = "536c3e33dae5f13314f7bb66"
    response = unirest.get(settings.API_URL + 'question/' + qid, headers={'Content-Type':'application/json'})
    datum = {"courses": ["Urban Policy and Planning"]}
    etag = response.body['_etag']

    response2 = unirest.patch(settings.API_URL +
            'question/' + qid,
            headers={'Accept':'application/json', 'If-Match': etag}, params=datum)
    print response2.body

if __name__ == '__main__':
    main()
