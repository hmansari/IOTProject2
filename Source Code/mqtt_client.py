# Import the Modules
#import paho.mqtt.client as mqtt
#import ibmiotf.device
import time
from datetime import datetime
import os, json
import ibmiotf.application
import uuid

client = None

def myCommandCallback(cmd):
  if cmd.event == "status":
    payload = json.loads(cmd.payload)
    #print payload
    if "Open" in payload:
      print str(datetime.now()) + " OPEN"
    elif "Close" in payload:
      print str(datetime.now()) + " CLOSE"
    #if payload["Open"]:
    #  print "Door is Opened"
    #else: 
    #  print "Door is Closed"

try:
  options = ibmiotf.application.ParseConfigFile("/home/ravikanth/Desktop/device.cfg")
  client = ibmiotf.application.Client(options)
  client.connect()
  client.deviceEventCallback = myCommandCallback
  client.subscribeToDeviceEvents(event="status")
  print("Connected..waiting for events...")
  while True:
  	time.sleep(0.2)

except ibmiotf.ConnectionException  as e:
  print(e)











