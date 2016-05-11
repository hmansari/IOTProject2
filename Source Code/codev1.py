#!/usr/bin/python

import smbus
import math
import time
import os, json
import ibmiotf.application

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

client = None

f1 = open("stationary-open", "a")

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

bus.write_byte_data(address, power_mgmt_1, 0)


try:
        options = ibmiotf.application.ParseConfigFile("/home/pi/device.cfg")
        client = ibmiotf.application.Client(options)
        client.connect()
        f1.write("G_X" + "   " + "G_Y" + "   " + "G_Z" + "   " + "A_X" + "   " + "A_Y" + "   " + "A_Z")
        f1.write("\n")
        while 1:
                print "gyro data"
                print "---------"

                gyro_xout = read_word_2c(0x43)
                gyro_yout = read_word_2c(0x45)
                gyro_zout = read_word_2c(0x47)



                print "gyro_xout: ", gyro_xout
                print "gyro_yout: ", gyro_yout
                print "gyro_zout: ", gyro_zout

                print "accelerometer data"
                print "------------------"

                accel_xout = read_word_2c(0x3b)
                accel_yout = read_word_2c(0x3d)
                accel_zout = read_word_2c(0x3f)

                accel_xout_scaled = accel_xout / 16384.0
                accel_yout_scaled = accel_yout / 16384.0
                accel_zout_scaled = accel_zout / 16384.0

                print "accel_xout: ", accel_xout
                print "accel_yout: ", accel_yout
                print "accel_zout: ", accel_zout

                print "\n"
                #if abs(gyro_yout) > 1000:

                f1.write(str(gyro_xout) + "   " + str(gyro_yout) + "   " + str(gyro_zout) + "   " + str(accel_xout) + "   " + str(accel_yout) + "   " + str(accel_zout))
                f1.write("\n")


                #myData = {'gyro_X' : gyro_xout, 'gyro_Y' : gyro_yout, 'gyro_Z' : gyro_zout, 'acc_X' : accel_xout, 'acc_Y' : accel_yout, 'acc_Z' : accel$

                #print "abs----", abs(x_rotation)
                #if abs(x_rotation) > 10: 
                if gyro_yout > 1000:
                        print "opening", gyro_yout
                        myData = {'gyro_X' : gyro_xout, 'gyro_Y' : gyro_yout, 'gyro_Z' : gyro_zout, 'acc_X' : accel_xout, 'acc_Y' : accel_xout, 'acc_Z' : accel_zout}
                        client.publishEvent("RPi", "b827eb051cbc", "opening", "json",  myData)
                elif gyro_yout < -1000:
                        print "closing", gyro_yout
                        myData = {'gyro_X' : gyro_xout, 'gyro_Y' : gyro_yout, 'gyro_Z' : gyro_zout, 'acc_X' : accel_xout, 'acc_Y' : accel_yout, 'acc_Z' : accel_zout}
                        client.publishEvent("RPi", "b827eb051cbc", "closing", "json",  myData)
                else:
                        myData = {'gyro_X' : gyro_xout, 'gyro_Y' : gyro_yout, 'gyro_Z' : gyro_zout, 'acc_X' : accel_xout, 'acc_Y' : accel_yout, 'acc_Z' : accel_zout}

                time.sleep(1.2)


except ibmiotf.ConnectionException  as e:
        print e

finally:
        f1.close()

