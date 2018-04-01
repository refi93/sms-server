# python sms-server
A simple SMS server made in Python. It's a server where you send SMS messages as requests, those are handled by the server's handlers and the server sends the corresponding response as an SMS. You can make easily your own handlers and register them.
To run properly it needs a GSM module (in my case Ai Thinker A6) connected to the serial port (hardcoded /dev/ttyUSB0).
All it currently does is to listen for incomming SMS messages in an eternal loop, process them, send the response and clear the SMS memory of the GSM module.

## Why?
I have a Nokia 3310 and I want to get the best user experience out of it!

## Available SMS handlers (SMS "apps"):

### Navigation 
you send an SMS message 
	```navigate "addressA" "addresB"```
to the phone number of your GSM module and you get a response containing the distance and compass bearing from addresA to addressB

## Running the project:

1. copy config.py.example to config.py, add your phone number to the whitelist in it and set the pin of the SIM card in the GSM module
2. install dependencies
	```pip install -r requirements.txt```
3. run the project by
	```sudo python3 -m sms_server.py```