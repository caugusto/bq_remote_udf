from __future__ import print_function
import base64
import json
import os
from twilio.rest import Client
import time
import datetime



def notification_handler(request):
    request_json = request.get_json()
    mode = request_json['userDefinedContext']['mode']
    calls = request_json['calls']
    if mode == "sms":
        return twilio_router(calls)
    return json.dumps({"Error in Request": request_json}), 400


def twilio_router(calls):
    try:

        return_value = []

        for call in calls:
            msg=call[0]
            #phone=call[1]

            print("Update msg: " + msg)
            #print("Phone to send text to: " + phone)

            ##############
            # Insert call here
            twilio_result = twilio_action(msg)
            print("TWILIO_RESULT= " + str(twilio_result))
            ##############

            return_value.append(str(twilio_result))
        return_json = json.dumps({"replies": return_value})
        return return_json
    except Exception as inst:
        return json.dumps( { "errorMessage": 'something unexpected in twilio_router function' } ), 400


def twilio_action(msg):
    try:
        import datetime
        now = datetime.datetime.now()
        print ("Current date and time : ")
        print (now.strftime("%Y-%m-%d %H:%M:%S"))

        TWILIO_ACCOUNT_SID="<YOUR_TWILIO_ACCOUNT_SID>"
        TWILIO_AUTH_TOKEN="<YOUR_TWILIO_AUTH_TOKEN>"

        mybody="Sent from BigQuery at " + now.strftime("%Y-%m-%d %H:%M:%S") + ". " + msg
        myfrom='+<YOUR_TWILIO_PHONE>'
        myto='+<YOUR_DESTINATION_PHONE>'

        
        account_sid = TWILIO_ACCOUNT_SID
        auth_token = TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        
        message = client.messages \
                        .create(
                             body=mybody,
                             from_=myfrom,
                             to=myto
                         )

        return message.sid
    except Exception as inst:
        return json.dumps( { "errorMessage": 'something unexpected in twilio_action function' } ), 400


