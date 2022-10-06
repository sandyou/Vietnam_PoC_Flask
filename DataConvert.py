import json
import requests


def GetToken():
    headers = {"Content-type": "application/json"}
    user = {"username": "api_user1",
            "userpassword": "óøùþñäõüõóoýÏñàù"}  # change config
    response = requests.post(
        "http://Noibo.shingmark:9090/api/v1/login/", headers=headers, json=user)
    token = response.json()["token"]
    return token


def Dataconverter(Originaldata):
    newdata = {'module': 'life_function',
               'value': {
                   'patientNo': Originaldata['patientNo'],
                   'deviceNo': Originaldata['deviceNo'],
                   'measureDate': Originaldata['measureDateTime'],
                   'measureItems': Originaldata['measureItems']
               }}
    return newdata
