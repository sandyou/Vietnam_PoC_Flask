import json
import logging
from progress.bar import Bar
from datetime import datetime
from flask import Flask, request, jsonify, redirect, url_for
from flask_apscheduler import APScheduler
import tokenrequests

# logging.basicConfig(level=logging.DEBUG, filename='log.txt',
#                     format='[%(asctime)s %(levelname)-8s] %(message)s',
#                     datefmt='%Y%m%d %H:%M:%S',force=True)
def Now_time():
    return str(datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f"))

# define app
app = Flask(__name__)

# define auto scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

# set scheduler


@scheduler.task('interval', id='do_job_1', seconds=10)
def DoRequestfromHIStoiMward():
    # Take a header
    print("["+Now_time()+" INFO ]Start update HIS to iMWard:")
    header = tokenrequests.CreateHeader(tokenrequests.GetToken())

    # Do request to getting area's bed_info from HIS
    print("["+Now_time()+" INFO ]Geting data from HIS")
    response_from_his = tokenrequests.GetdatafromHIS_request(header)

    # Do request to update bed_info to iMward
    print("["+Now_time()+" INFO ]Do update to iMWard")
    bar = Bar('Processing', max=len(response_from_his['data']))
    # Do Data Converter and request update to iMward
    for i in response_from_his['data']:
        body = tokenrequests.HIStoiMward_Dataconverter(i)
        respons = tokenrequests.UpdateiMward_request(body)
        if respons != str(200):
            print("["+Now_time()+" ERROR ]Update to iWard occured Error")
        logging.info("Bed number:"+i['bedNum']+" Update response is : "+respons)
        bar.next()
        print("\n")
    bar.finish()
    print("["+Now_time()+" INFO ]Finish Bed iMWard info Update")


# set Flask service router


@app.route("/", methods=['POST'])
def getimvs():
    content = request.get_json(force=True)
    logging.info("iMVS data is:"+json.dumps(content))
    print("["+Now_time()+" INFO ]Access iMVSdata, Do request to HIS")
    res = tokenrequests.UpdateHIS_request(content)
    print("["+Now_time()+" INFO ]request from HIS : "+res.text)
    return res.text


@app.route('/<path:text>', methods=['POST'])
def all_routes(text):
    if text.startswith('http://127.0.0.1'):
        return redirect(url_for('getimvs'))
    else:
        return redirect(url_for('404_error'))


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    scheduler.start()
    app.run(host='0.0.0.0', port=8070)
