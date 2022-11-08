import sys
import requests
import logging
import configparser
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# logging.basicConfig(level=logging.DEBUG, filename='request.log', filemode='a',
#                     format='[%(asctime)s %(levelname)-8s] %(message)s',
#                     datefmt='%Y%m%d %H:%M:%S')

try:
    appconfig = configparser.ConfigParser()
    appconfig.read('config.ini')
    His_link = appconfig.get('link', 'His_link')
except Exception as error:
    logging.error(error)
    print("Config error when catch HIS link, please check configfile!!")
    sys.exit()


logging.basicConfig(
    handlers=[
        TimedRotatingFileHandler('uvicorn_server.log',
                                 when='d', interval=3, backupCount=5)],
    level=logging.DEBUG,
    format='[%(asctime)s %(levelname)-8s] %(message)s',
    datefmt='%Y%m%d %H:%M:%S')


def setup_logger(name, log_file, level=logging.DEBUG):
    """To setup as many loggers as you want"""
    handle = TimedRotatingFileHandler(
        log_file, when='d', interval=3, backupCount=5)
    handle.setFormatter(logging.Formatter(
        "[%(asctime)s %(levelname)-s] %(message)s",
        "%Y-%m-%d %H:%M:%S"))
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handle)
    return logger


def Now_time():
    return str(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))


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
