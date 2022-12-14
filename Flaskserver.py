import json
import logging
import configparser
import sys

from urllib3 import make_headers

import Make_header
import iMWard
import iMVS

from flask import Flask, request, jsonify, redirect, url_for
from flask_apscheduler import APScheduler

# check config
appconfig = configparser.ConfigParser()
try:
    appconfig.read('config.ini')
    appconfig.get('health device', 'iMVS')
    appconfig.get('health device', 'iMWard')
    UpadateTime = appconfig.get('health device', 'iMWard_updatetime')
except Exception as error:
    logging.error(error)
    print("Config error please check configfile!!")
    sys.exit()

    # define app
app = Flask(__name__)

# define auto scheduler
scheduler = APScheduler()
scheduler.api_enabled = True

# set scheduler

if appconfig.get('health device', 'iMWard') == "True":
    @scheduler.task('interval', id='do_job_1', seconds=int(UpadateTime))
    def DoRequestfromHIStoiMward():
        iMWard.Doloop_UpdatetoiMWard()

# set Flask service router


@ app.route("/", methods=['POST'])
def getimvs():
    content = request.get_json(force=True)
    print("["+Make_header.Now_time()+" IMVS ]Access iMVSdata, Do request to HIS")
    res = iMVS.UpdateHIS_request(content)
    print("["+Make_header.Now_time()+" IMVS ]request from HIS : "+res)
    return res


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0', port=8070)
