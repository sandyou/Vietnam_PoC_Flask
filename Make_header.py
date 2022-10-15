import json
import requests
import logging
import configparser
from datetime import datetime

# Config link Path
try:
    appconfig = configparser.ConfigParser()
    appconfig.read('config.ini')
    His_link = appconfig.get('link', 'His_link')
except Exception as error:
    logging.error(error)
    print("Config error when catch HIS link, please check configfile!!")
    quit()

# setting logging config
logging.basicConfig(level=logging.DEBUG, filename='request.log', filemode='w',
                    format='[%(asctime)s %(levelname)-8s] %(message)s',
                    datefmt='%Y%m%d %H:%M:%S')


def Now_time():
    return str(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))


def CreateHeader(token):
    headers = {"Content-type": "application/json",
               "Authorization": "Bearer " + token}
    return headers


def GetToken():
    headers = {"Content-type": "application/json"}
    user = {"username": "api_user1",
            "userpassword": "óøùþñäõüõóoýÏñàù"}  # change config
    response = requests.post(
        "http://"+His_link+":9090/api/v1/login/", headers=headers, json=user)
    token = response.json()["token"]
    return token


def Do_requesttoHIS(header, body):
    response = requests.post(
        "http://"+His_link+":9090/api/v1/", headers=header, json=body)
    return response
