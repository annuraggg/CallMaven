import json
import os
from flask import Flask, jsonify, redirect, request
from apis.database_api import Users, Tickets, Calls

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
from twilio.rest import Client

from dotenv import load_dotenv

from admin.route_handler import admin
from employee.route_handler import employee
from customer.route_handler import customer
from apis.route_handler import apis

from datetime import datetime

import apis.database_api as db

app = Flask(__name__, static_folder='static')
app.config['JWT_SECRET'] = os.getenv("JWT_SECRET")
load_dotenv()

# ROUTES
for bp in [admin, employee, customer, apis]:
    app.register_blueprint(bp)


account_sid = os.environ['TWILIO_ACCOUNT_SID']
api_key = os.environ['TWILIO_API_KEY_SID']
api_key_secret = os.environ['TWILIO_API_KEY_SECRET']
twiml_app_sid = os.environ['TWIML_APP_SID']
twilio_number = os.environ['TWILIO_NUMBER']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

print(account_sid)
print(api_key)
print(api_key_secret)
print(twiml_app_sid)
print(twilio_number)
print(auth_token)


@app.route('/', methods=['GET'])
def get_home():
    return redirect('/employee')


@app.route('/token', methods=['GET'])
def get_token():
    identity = twilio_number
    outgoing_application_sid = twiml_app_sid

    access_token = AccessToken(account_sid, api_key,
                               api_key_secret, identity=identity)

    voice_grant = VoiceGrant(
        outgoing_application_sid=outgoing_application_sid,
        incoming_allow=True,
    )
    access_token.add_grant(voice_grant)

    response = jsonify(
        {'token': access_token.to_jwt(), 'identity': identity})

    return response


@app.route('/handle_calls', methods=['POST'])
def call():
    response = VoiceResponse()
    dial = Dial(callerId=twilio_number)
    if 'To' in request.form and request.form['To'] != twilio_number:
        dial.number(request.form['To'])
    else:
        caller = request.form['Caller']
        dial = Dial(callerId=caller)
        dial.client(twilio_number)

    return str(response.append(dial))


@app.route('/getCall', methods=['POST'])
def getCalls():
    client = Client(account_sid, auth_token)
    call = client.calls(request.form['sid']).fetch()
    type = call.direction

    call_dict = {
        'sid': request.form['sid'],
        'to': request.form['to'],
        'from': int(request.form['from']),
        'status': call.status,
        'start_time': call.start_time,
        'end_time': call.end_time,
        'duration': call.duration,
        'direction': type.title(),
    }

    print(call_dict)

    callAdd = Calls.insert_one(call_dict)
    if (callAdd):
        return ("True")
    else:
        return ("False")
