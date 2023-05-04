#!/usr/bin/env python3

import base64
import configparser
from datetime import datetime
import json

import paho.mqtt.client as mqtt

import parser

# Read in config file with MQTT details.
config = configparser.ConfigParser()
config.read("config.ini")

# MQTT broker details
broker_address = config["mqtt"]["broker"]
username = config["mqtt"]["username"]
password = config["mqtt"]["password"]

# MQTT topic to subscribe to. We subscribe to all uplink messages from the
# devices.
topic = "v3/+/devices/+/up"

# Callback when successfully connected to MQTT broker.
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker.")

    if rc != 0:
        print(" Error, result code: {}".format(rc))


# Callback function to handle incoming MQTT messages
def on_message(client, userdata, message):
    # Timestamp on reception.
    current_date = datetime.now()

    # Handle TTN packet format.
    message_str = message.payload.decode("utf-8")
    message_json = json.loads(message_str)
    encoded_payload = message_json["uplink_message"]["frm_payload"]
    raw_payload = base64.b64decode(encoded_payload)

    if len(raw_payload) == 0:
        # Nothing we can do with an empty payload.
        return

    # First byte should be the group number, remaining payload must be parsed.
    #print("RAW PAYLOAD: ", raw_payload)
    #print("FIRST BYTE: ", hex(raw_payload[0]))
    #print("SECOND BYTE: ", hex(raw_payload[1]))
    #print("THIRD BYTE: ", hex(raw_payload[2]))
    #print("FOURTH BYTE: ", hex(raw_payload[3]))
    #print("FIFTH BYTE: ", hex(raw_payload[4]))
    #print("SIXTH BYTE: ", hex(raw_payload[5]))
    #print("SEVENTH BYTE: ", hex(raw_payload[6]))
    #group_number = raw_payload[0]
    #remaining_payload = raw_payload[1:]

    # See if we can decode this payload.
    try:
        works = parser.decode(raw_payload)
    except:
        print("Failed to decode payload.")
        return

    if works == None:
        print("Undecoded message.")
    else:
        print("GPS data received.")

# MQTT client setup
client = mqtt.Client()

# Setup callbacks.
client.on_connect = on_connect
client.on_message = on_message

# Connect to broker.
client.username_pw_set(username, password)
client.tls_set()
client.connect(broker_address, 8883)

# Subscribe to the MQTT topic and start the MQTT client loop
client.subscribe(topic)
client.loop_forever()
#!/usr/bin/env python3
