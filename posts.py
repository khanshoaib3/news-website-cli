import json
import requests
from requests.structures import CaseInsensitiveDict
from texttable import Texttable

def allPosts():
    url = "https://blindcraft.pythonanywhere.com/news/api/getPost/"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    dictionary = {'typeOf':'all'}
    data = json.dumps(dictionary, indent=4)

    resp = requests.get(url, headers=headers, data=data)
    data = json.loads(resp.text)
    return data['data']

def userPosts(id):
    url = "https://blindcraft.pythonanywhere.com/news/api/getPost/"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    dictionary = {'typeOf':'Token '+id}
    data = json.dumps(dictionary, indent=4)
    resp = requests.get(url, headers=headers, data=data)
    data = json.loads(resp.text)
    return data['data']

def singlePost(id):
    url = "https://blindcraft.pythonanywhere.com/news/api/getPost/"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    dictionary = {'typeOf':''+id}

    data = json.dumps(dictionary, indent=4)
    resp = requests.get(url, headers=headers, data=data)

    try:
        data = json.loads(resp.text)

        t = Texttable()
        data['data'].insert(0,['ID','Title','Slug','Body','Thumbnail','User ID','Publish','Created','Updated','Status'])
        t.add_rows(data['data'])
        print(t.draw())
    except:
        print((resp.text))


