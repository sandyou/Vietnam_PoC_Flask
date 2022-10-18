import json
import logging

import Make_header

imvs_log = Make_header.setup_logger('imvs', 'imvs_request.log')


def UpdateHIS_request(data):
    imvs_log.info("From iMVS data is:"+json.dumps(data))
    headers = Make_header.CreateHeader(Make_header.GetToken())
    con_data = iMVStoHIS_DataConverter(data)
    imvs_log.info("UpdateHIS_request header is:"+json.dumps(headers))
    imvs_log.info("UpdateHIS_request Data is:"+json.dumps(con_data))
    try:
        response2 = Make_header.Do_requesttoHIS(headers, con_data)
    except Exception as error:
        imvs_log.error(error)
        print("have error when update iMVS data to HIS")
    imvs_log.info("patientNo "+con_data['value']['patientNo'] +
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
