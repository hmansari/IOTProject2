README
*****************************************************************************************************
1) Update system packages
	sudo apt-get update && sudo apt-get upgrade
2) Install Bluemix IoT Library for Python
	curl –LO https://github.com/ibm-messaging/iot-raspberrypi/releases/download/1.0.2.1/iot_1.0-2_armhf.deb
	sudo dpkg –i iot_1.0-2_armhf.deb
3) Get Device ID
	service iot getdeviceid
4) Create a config file for the device using the details from Bluemix after registering the device
	sudo nano /etc/iotsample-raspberrypi/device.cfg
5) Service Restart
	sudo service iot restart
5) To run the code
	cd /home/pi/Desktop/Project
	python codev1.py
