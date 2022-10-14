import json
from datetime import datetime
from wsgiref import headers
import requests
import logging

# Config link Path
# His_link = 'Noibo.shingmark'
His_link = '115.75.7.105'
iMward_link = '127.0.0.1'

# setting logging config
logging.basicConfig(level=logging.DEBUG, filename='request.log', filemode='w',
                    format='[%(asctime)s %(levelname)-8s] %(message)s',
                    datefmt='%Y%m%d %H:%M:%S')

def UpdateiMward_request(data):
    # logging.info("UpdateiMward_request header is:"+header)
    header = {"Content-type": "application/json"}
    logging.info("UpdateiMward_request Data is:"+json.dumps(data['datalist'][0]['bedNum']))
    try:
        # response2 = requests.post(
        #     "http://" + iMward_link + ":5000/InsertBedInfo", headers=header, json=data)
        response2 = requests.post(
            "http://"+iMward_link+":5000/UpdateBedInfo", headers=header, json=data)
    except Exception as error:
        logging.error(str(error))
        return 'Request Error'
    return str(response2.status_code)


def GetdatafromHIS_request(header):
    body = {'module': 'department_info',
            'value': {'Khoa': 'KUB'}}
    response2 = requests.post(
        "http://"+His_link+":9090/api/v1/", headers=header, json=body)
    return response2.json()


def UpdateHIS_request(data):
    headers = CreateHeader(GetToken())
    con_data = iMVStoHIS_DataConverter(data)
    logging.info("UpdateHIS_request header is:"+json.dumps(headers))
    logging.info("UpdateHIS_request Data is:"+json.dumps(con_data))
    #print("To HIS:", con_data)
    response2 = requests.post(
        "http://"+His_link+":9090/api/v1/", headers=headers, json=con_data)
    return response2


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

def DateConverter(Originaltime):
    if Originaltime == "":
        return Originaltime
    else:
        time = datetime.strptime(Originaltime[:-3], '%m/%d/%Y %H:%M:%S')
        New_time = time.strftime("%Y-%m-%d")
        return New_time

def iMVStoHIS_DataConverter(Originaldata):
    newdata = {'module': 'life_function',
               'value': {
                   'patientNo': Originaldata['patientNo'],
                   'deviceNo': Originaldata['deviceNo'],
                   'measureDate': Originaldata['measureDateTime'],
                   'measureItems': Originaldata['measureItems']
               }}
    return newdata


def HIStoiMward_Dataconverter(Originaldata):
    newData = {
        "datalist": [{"patientName": Originaldata['patientName'],
                      "age":Originaldata['age'],
                      "birthDate":DateConverter(Originaldata['birthDate']),
                      "gender":Originaldata['gender'],
                      "bedNum":Originaldata['bedNum'],
                      "inPatientNum":Originaldata['inPatientNum'][0:20],
                      "mainDoc":Originaldata['mainDoc'][0:16],
                      "nurse":Originaldata['nurse'][0:16],
                      "nurse2":Originaldata['nurse2'],
                      "inDoc":Originaldata['inDoc'][0:16],
                      "precaution":Originaldata['precaution'],
                      "inDepartDate":DateConverter(Originaldata['inDepartDate']),
                      "outDepartDate":DateConverter(Originaldata['outDepartDate']),
                      "nursingLevel":Originaldata['nursingLevel'],
                      "area":Originaldata['area'],
                      "operationDate":Originaldata['operationDate'],
                      "property1":Originaldata['property1'],
                      "property2":Originaldata['property2'],
                      "property3":Originaldata['property3'],
                      "property4":Originaldata['property4'],
                      "property5":Originaldata['property5'],
                      "diastolicBloodPressure":Originaldata['diastolicBloodPressure'],
                      "systolicBloodPressure":Originaldata['systolicBloodPressure'],
                      "bodyTemperature":Originaldata['bodyTemperature'],
                      "height":Originaldata['height'],
                      "weight":Originaldata['weight']
                      }],
        "tenant_nammme": "t1"
    }

    return newData