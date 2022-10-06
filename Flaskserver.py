import logging
import requests
from flask import has_request_context, request
from flask.logging import default_handler
from flask import Flask, request, jsonify, redirect, url_for
import tokenrequests

app = Flask(__name__)


@app.route("/", methods=['POST'])
def getimvs():
    content = request.get_json(force=True)
    #print("get imvs contents:", content)
    #print("Do request to HIS")
    res = tokenrequests.Dorequest(content)
    # print(res.text)
    return res.text


@app.route('/<path:text>', methods=['POST'])
def all_routes(text):
    if text.startswith('http://127.0.0.1'):
        return redirect(url_for('getimvs'))
    else:
        return redirect(url_for('404_error'))


if __name__ == "__main__":
    app.config['JSON_AS_ASCII'] = False
    logging.basicConfig(filename='error.log', level=logging.DEBUG)
    app.run(host='0.0.0.0', port=8080)
