from flask import Flask,redirect
from flask import render_template
from flask import request
import os, json
import time
import ibmiotf.application
import subprocess


client = None
deviceId = os.getenv("DEVICE_ID")
vcap = json.loads(os.getenv("VCAP_SERVICES"))

# os.chdir("libsvm-3.21")
os.system("make")

# cmd1 = 'cd /home/vcap/app/python'
# cmd2 = 'make'
# cmd3 = 'python classify.py'
# # cmd4 = 'cd /home/vcap/app'
# final = Popen("{}; {}; {}".format(cmd1, cmd2, cmd3), shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
# stdout, nothing = final.communicate()
# print stdout

G_X = []
G_Y = []
G_Y_close = []
G_Z = []
A_X = []
A_Y = []
A_Z = []

def analyze(gy):
        sumGY = 0
        average_GY = 0
        for n2 in gy:
            sumGY = sumGY + n2
            average_GY = sumGY / len(gy)
        # print "average is ", average_GY
        # f1 = open("test", "a")
        if average_GY > 0:
            # print "++++++++"
            f1 = open("test", "w")
            f1.write("1 " + "1:" + str(average_GY))
            f1.close()
        elif average_GY < 0:
            # print "--------"
            f1 = open("test", "w")
            f1.write("-1 " + "1:" + str(average_GY))
            f1.close()
        
        # print "++++++++"
        subprocess.check_output("./svm-train -t 2 -c 2.0 -g 0.000030517 train",stderr=subprocess.STDOUT,shell=True)
        subprocess.check_output("./svm-predict test train.model result",stderr=subprocess.STDOUT,shell=True)
        f2 = open("result", "r")
        prev = "1"
        for i in f2.readline():
            # print i
            # print prev
            if i == "1" and prev != "-":
                print "OPEN"
                myData = {'Open' : "OPEN"}
                client.publishEvent("DoorStatusDisplay", "0000abcd", "status", "json", myData)
                time.sleep(0.2)
            elif i == "-":
                print "CLOSE"
                myData = {'Close' : "CLOSE"}
                client.publishEvent("DoorStatusDisplay", "0000abcd", "status", "json", myData)
                time.sleep(0.2)
            prev = i
        f2.close()

def myCommandCallback(cmd):
    global G_X
    global G_Y
    global G_Y_close
    global G_Z
    global A_X
    global A_Y
    global A_Z

    if cmd.event == "opening":
        payload = json.loads(cmd.payload)
        G_X.append(int(payload["gyro_X"]))
        G_Y.append(int(payload["gyro_Y"]))
        G_Z.append(int(payload["gyro_Z"]))
        A_X.append(int(payload["acc_X"]))
        A_Y.append(int(payload["acc_Y"]))
        A_Z.append(int(payload["acc_Z"]))
        # print "opening", G_Y
        # time.sleep(2)
        analyze(G_Y)


    elif cmd.event == "closing":
        payload = json.loads(cmd.payload)
        G_Y_close.append(int(payload["gyro_Y"]))
        analyze(G_Y_close)

   

try:
    options = {
        "org": vcap["iotf-service"][0]["credentials"]["org"],
        "id": vcap["iotf-service"][0]["credentials"]["iotCredentialsIdentifier"],
        "auth-method": "apikey",
        "auth-key": vcap["iotf-service"][0]["credentials"]["apiKey"],
        "auth-token": vcap["iotf-service"][0]["credentials"]["apiToken"]
    }
    client = ibmiotf.application.Client(options)
    client.connect()

    client.deviceEventCallback = myCommandCallback
    client.subscribeToDeviceEvents(event="opening")
    client.subscribeToDeviceEvents(event="closing")
    client.subscribeToDeviceEvents(event="still")

except ibmiotf.ConnectionException as e:
    print e

app = Flask(__name__)
port = os.getenv('VCAP_APP_PORT', '5000')

@app.route('/')
def hello():
	return '<!doctype html>\n<html><head><title>Hello from Flask</title></head><body><h1>Sensor Information</h1> <br /> <br /> <form action="/status" method="POST"> </form> </body></html>'


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
