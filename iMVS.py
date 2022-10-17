import json
import logging

import Make_header


def UpdateHIS_request(data):
    headers = Make_header.CreateHeader(Make_header.GetToken())
    con_data = iMVStoHIS_DataConverter(data)
    logging.info("UpdateHIS_request header is:"+json.dumps(headers))
    logging.info("UpdateHIS_request Data is:"+json.dumps(con_data))
    try:
        response2 = Make_header.Do_requesttoHIS(headers, con_data)
    except Exception as error:
        logging.error(error)
        print("have error when update iMVS data to HIS")
    logging.info("patientNo "+con_data['value']['patientNo'] +
                 " data update to HIS is success!!")
    return response2


def iMVStoHIS_DataConverter(Originaldata):
    # execute PatientNo
    if len(Originaldata['patientNo']) == 9:
        patientno = Originaldata['patientNo'][0:2] + \
            '.'+Originaldata['patientNo'][2:]
    else:
        patientno = Originaldata['patientNo']

    newdata = {'module': 'life_function',
               'value': {
                   'patientNo': patientno,
                   'deviceNo': Originaldata['deviceNo'],
                   'measureDate': Originaldata['measureDateTime'],
                   'measureItems': Originaldata['measureItems']
               }}
    return newdata
