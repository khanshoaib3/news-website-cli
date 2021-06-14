import json
import requests
import os
from requests.structures import CaseInsensitiveDict
from main import setToken


def login(username,password):
    url = "https://blindcraft.pythonanywhere.com/account/api/signin/"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    dictionary = {'username':username,'password':password}
    data = json.dumps(dictionary, indent=4)

    resp = requests.post(url, headers=headers, data=data)

    return_data = json.loads(resp.text)

    if 'Token' in return_data.keys():
        setToken(return_data['Token'])
        return "Login successful"
    else:
        return ""+return_data['Error']


def logout():
    if os.path.exists('.cred'):
        os.remove('.cred')

def signup(email, username, password, c_password, name):
    url = "https://blindcraft.pythonanywhere.com/account/api/signup/"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"

    dictionary = {
            'email':email,
            'username':username,
            'password':password,
            'confirmPassword':c_password,
            'firstName':name}
    data = json.dumps(dictionary, indent=4)

    resp = requests.post(url, headers=headers, data=data)

    return_data = json.loads(resp.text)

    if 'Token' in return_data.keys():
        setToken(return_data['Token'])
        return "Account created successfully!!"
    else:
        try:
            return ""+return_data['Error']
        except:
            return "Please provide all fields"
