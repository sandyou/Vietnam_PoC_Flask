import json
import logging

import Make_header


def UpdateHIS_request(data):
    headers = Make_header.CreateHeader(Make_header.GetToken())
    con_data = iMVStoHIS_DataConverter(data)
    logging.info("UpdateHIS_request header is:"+json.dumps(headers))
    logging.info("UpdateHIS_request Data is:"+json.dumps(con_data))
    response2 = Make_header.Do_requesttoHIS(headers, con_data)
    return response2


def iMVStoHIS_DataConverter(Originaldata):
    newdata = {'module': 'life_function',
               'value': {
                   'patientNo': Originaldata['patientNo'],
                   'deviceNo': Originaldata['deviceNo'],
                   'measureDate': Originaldata['measureDateTime'],
                   'measureItems': Originaldata['measureItems']
               }}
    return newdata
