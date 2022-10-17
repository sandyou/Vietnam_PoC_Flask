import json
import logging
import configparser

import Make_header
import iMWard
import iMVS

from flask import Flask, request, jsonify, redirect, url_for
from flask_apscheduler import APScheduler

'''
    advance:
    check is new bednum
'''

# check config
appconfig = configparser.ConfigParser()
try:
    appconfig.read('config.ini')
    appconfig.get('health device', 'iMVS')
    appconfig.get('health device', 'iMWard')
except Exception as error:
    logging.error(error)
    print("Config error please check configfile!!")
    quit()

    # define app
app = Flask(__name__)

# define auto scheduler
scheduler = APScheduler()
scheduler.api_enabled = True

# set scheduler

if appconfig.get('health device', 'iMWard') == "True":
    @scheduler.task('interval', id='do_job_1', seconds=60)
    def DoRequestfromHIStoiMward():
        iMWard.Doloop_UpdatetoiMWard()

# set Flask service router


@ app.route("/", methods=['POST'])
def getimvs():
    content = request.get_json(force=True)
    logging.info("iMVS data is:"+json.dumps(content))
    print("["+Make_header.Now_time()+" INFO ]Access iMVSdata, Do request to HIS")
    res = iMVS.UpdateHIS_request(content)
    print("["+Make_header.Now_time()+" INFO ]request from HIS : "+res.text)
    return res.text


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=8070)
