import json
import requests
import logging

logging.basicConfig(level=logging.DEBUG, filename='log.txt',
                    format='[%(asctime)s %(levelname)-8s] %(message)s',
                    datefmt='%Y%m%d %H:%M:%S')

link = 'Noibo.shingmark'

def Dorequest(data):
    token = GetToken()
    headers = {"Content-type": "application/json",
               "Authorization": "Bearer " + token}
    con_data = DataConverter(data)
    logging.info("header is:"+headers)
    logging.info("Data is:"+con_data)
    #print("To HIS:", con_data)
    response2 = requests.post(
        "http://"+link+":9090/api/v1/", headers=headers, json=con_data)
    return response2


def GetToken():
    headers = {"Content-type": "application/json"}
    user = {"username": "api_user1",
            "userpassword": "óøùþñäõüõóoýÏñàù"}  # change config
    response = requests.post(
        "http://"+link+":9090/api/v1/login/", headers=headers, json=user)
    token = response.json()["token"]
    print("token:", token)
    return token


def DataConverter(Originaldata):
    newdata = {'module': 'life_function',
               'value': {
                   'patientNo': Originaldata['patientNo'],
                   'deviceNo': Originaldata['deviceNo'],
                   'measureDate': Originaldata['measureDateTime'],
                   'measureItems': Originaldata['measureItems']
               }}
    return newdata
