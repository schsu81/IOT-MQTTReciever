#!/nhome/schsu/miniconda3/envs/iot/bin/python3
##!/usr/bin/env python3
# %% ===========================================================================================
import paho.mqtt.client as mqtt
from datetime import datetime
try:
  from .llib import *
  from .config import *
except ImportError:
  from llib import *
  from config import *
# %% ===========================================================================================
def on_connect(client, userdata, flags, rc, properties=None):
    from __main__ import MQTT_TOPIC
    if rc == 0:
        print("Connected successfully.")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribe {MQTT_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}")
# ------------------------------------------------------------------------------------        
def on_message(client, userdata, message):
    #print(f"Message received on topic {message.topic}: {message.payload.decode()}")
    from __main__ import DATA_DIR
    encoded_data = message.payload.decode()
    parsed_data  = decode_and_parse_sensor_data(encoded_data)
    if not 'error' in parsed_data:
      parsed_data['datetime'] = datetime.fromtimestamp(parsed_data['timestamp'])
      print(f"Parsed Data Dictionary: {parsed_data['datetime']} id={parsed_data['id']} smac={parsed_data['station_mac']} sname={parsed_data['station_name']}")

      if isinstance(Stations,list):
        if (parsed_data['station_mac'] in Stations) or (parsed_data['station_name'] in Stations):
          fn = outFileName(parsed_data)
          writeFile(fn,parsed_data,DATA_DIR=DATA_DIR,format='csv')
      else:
        fn = outFileName(parsed_data)
        writeFile(fn,parsed_data,DATA_DIR=DATA_DIR,format='csv')
    else:
      print(parsed_data)
    try:
      from __main__ import message_received
      message_received.append(parsed_data)
    except:
      pass

# %% ===========================================================================================
#Set up MQTT client
mqtt_client = mqtt.Client() 
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set(MQTT_USER, MQTT_PW)  # Set MQTT username and password

# Connect to MQTT Broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start the loop
mqtt_client.loop_forever()

# debug code
# message_received = []
# mqtt_client.loop_start()
# while len(message_received)<1:
#   pass
# mqtt_client.loop_stop()

print('loop stopped')

# %% ===========================================================================================

