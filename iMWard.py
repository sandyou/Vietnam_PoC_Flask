import logging
import json
import re
import requests
import configparser
import sys

import Make_header

from datetime import datetime
from wsgiref import headers
from progress.bar import Bar


imward_log = Make_header.setup_logger('imward', 'imward_request.log')
# Config link Path
try:
    appconfig = configparser.ConfigParser()
    appconfig.read('config.ini')
    iMward_link = appconfig.get('link', 'iMward_link')
except Exception as error:
    imward_log.error(error)
    print("Config error when catch iMward link and mode, please check configfile!!")
    sys.exit()


def Doloop_UpdatetoiMWard():
    print("["+Make_header.Now_time()+" IMWARD ]Start update HIS to iMWard:")
    header = Make_header.CreateHeader(Make_header.GetToken())

    # Do request to getting area's bed_info from HIS
    print("["+Make_header.Now_time()+" IMWARD ]Geting data from HIS")
    response_from_his = GetdatafromHIS_request(header)

    # Do request to update bed_info to iMward
    print("["+Make_header.Now_time()+" IMWARD ]Do update to iMWard")
    bar = Bar('Processing', max=len(response_from_his['data']))

    # Do Data Converter and request update to iMward
    for i in response_from_his['data']:
        body = HIStoiMward_Dataconverter(i)
        respons = UpdateiMward_request(True, body)
        if respons != 'Connection Error' and respons != 'Request Error' and len(respons.json()["error_bed"]) == 1:
            respons = UpdateiMward_request(False, body)
        if respons != 'Connection Error' and respons != 'Request Error' and len(respons.json()["error_bed"]) == 1:
            print("["+Make_header.Now_time()+" IMWARD ]Somthing Error!!")
        else:
            imward_log.info(
                "Finish " + body['datalist'][0]['bedNum']+" update!!")
        bar.next()
    bar.finish()
    print("["+Make_header.Now_time()+" IMWARD ]Finish Bed iMWard info Update")


def UpdateiMward_request(IsUpdate, data):
    # logging.info("UpdateiMward_request header is:"+header)
    header = {"Content-type": "application/json"}
    imward_log.info("UpdateiMward_request Data is:" +
                    json.dumps(data['datalist'][0]['bedNum']))
    # imward_log.info(data)
    try:
        if IsUpdate == False:
            response2 = requests.post(
                "http://" + iMward_link + ":5000/InsertBedInfo", headers=header, json=data, timeout=2)
        else:
            response2 = requests.post(
                "http://"+iMward_link+":5000/UpdateBedInfo", headers=header, json=data, timeout=2)
    except requests.exceptions.ConnectionError as e:
        imward_log.error(e)
        print("["+Make_header.Now_time() +
              " IMWARD ]has error when connection to : "+iMward_link)
        return 'Connection Error'
    except Exception as error:
        imward_log.error(error)
        print("["+Make_header.Now_time()+" IMWARD ]have error when update to imward, header is:" +
              header + ", Content is : "+data+'\n')
        return 'Request Error'
    return response2


def GetdatafromHIS_request(header):
    body = {'module': 'department_info',
            'value': {'Khoa': 'KUB'}}
    response2 = Make_header.Do_requesttoHIS(header, body)
    return response2.json()


def DateConverter(Originaltime):
    if Originaltime == "":
        return Originaltime
    else:
        time = datetime.strptime(Originaltime[:-3], '%m/%d/%Y %H:%M:%S')
        New_time = time.strftime("%Y-%m-%d")
        return New_time


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
                      "operationDate":DateConverter(Originaldata['operationDate']),
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
        "tenant_name": "t1"
    }

    return newData
