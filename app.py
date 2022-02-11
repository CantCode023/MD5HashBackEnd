import traceback
from flask import Flask, request
import re
import hashlib
import smtplib
import requests
import json
from flask_cors import CORS

usr = "frostbot023@gmail.com"
pswd = "Apakah?##5"

app = Flask(__name__)
CORS(app)

@app.route("/home")
def home():
    return "Home"

@app.route("/check/<string>")
def checker(string):
    # get path parameter called string with Flask
    md5 = str(request.view_args['string'])
    matched = re.match(r"[a-f0-9]{32}", md5)
    print(matched)
    print(md5)
    if matched != None:
        return str(matched.group() == md5)
    else:
        return "False"

@app.route("/gen/<string>")
def generator(string):
    # get query parameter called string
    string = request.view_args['string']
    # convert string to md5 using hashlib
    md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
    return str(md5)

@app.route("/sendEmail")
def sendEmail():
    # get query parameter called name
    name = request.args.get('name')
    email = request.args.get('email')
    message = request.args.get('message')
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

    payload = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": "md5hashofficial@gmail.com"
                    }
                ],
                "subject": "MD5 Contact"
            }
        ],
        "from": {
            "email": email
        },
        "content": [
            {
                "type": "text/plain",
                "value": f"Name: {name}\nEmail: {email}\n\n{message}"
            }
        ]
    }    

    headers = {
        'content-type': "application/json",
        'x-rapidapi-host': "rapidprod-sendgrid-v1.p.rapidapi.com",
        'x-rapidapi-key': "8ee4a2a0ebmshc758cdfc9769e70p1c9e26jsn710476d3e649"
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    if response.status_code == 202:
        print('e')
        return "Email sent!"
    else:
        print(traceback.format_exc())
        return "Something went wrong!"