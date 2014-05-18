def post():
    url = "http://127.0.0.1:5000/post"
    post = {}

def main():
    print "hello world"

data = urllib.urlencode(course)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()
print the_page

if __name__ == "__main__":
    main()
