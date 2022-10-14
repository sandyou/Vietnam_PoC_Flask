import json
import logging

import Make_header
import iMWard
import iMVS

from flask import Flask, request, jsonify, redirect, url_for
from flask_apscheduler import APScheduler


# define app
app = Flask(__name__)

# define auto scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

# set scheduler


@scheduler.task('interval', id='do_job_1', seconds=300)
def DoRequestfromHIStoiMward():
    iMWard.Doloop_UpdatetoiMWard()

# set Flask service router


@app.route("/", methods=['POST'])
def getimvs():
    content = request.get_json(force=True)
    logging.info("iMVS data is:"+json.dumps(content))
    print("["+Make_header.Now_time()+" INFO ]Access iMVSdata, Do request to HIS")
    res = iMVS.UpdateHIS_request(content)
    print("["+Make_header.Now_time()+" INFO ]request from HIS : "+res.text)
    return res.text


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    scheduler.start()
    app.run(host='0.0.0.0', port=8070)
