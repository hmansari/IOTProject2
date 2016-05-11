README
*****************************************************************************************************
1) Install ibmiotf libraries using:
	sudo pip install ibmiotf
2) Install dependencies:
	sudo pip install json
	sudo pip install simplejson
	sudo pip install django
3) Get Device ID
	service iot getdeviceid
4) Create a config file for the device using the details from Bluemix after registering the device
5) Now run the script "mqtt_client.py"
- The client shows "INFO Connected Successfully" if the connection was successful
- Now whenever a door open/close event occurs, it is displayed on the client

