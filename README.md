IoT Temperature Monitoring System
This project implements an IoT solution for monitoring room temperature in a hotel setting. It consists of three main components: a publisher that simulates temperature sensor readings, a subscriber that processes these readings and raises alarms, and a server that exposes the data via an HTTP API.

Prerequisites:

Python 3.7 or higher
MQTT broker installed and running on localhost:1883


Usage:

Start the publisher:
python publisher.py

In a new terminal, start the subscriber:
python subscriber.py

In another terminal, start the server:
python server.py

To get the latest temperature reading, make a GET request to http://localhost:5000/temperature

Configuration:

You can adjust the following parameters in the code:-

MQTT_BROKER and MQTT_PORT in publisher.py and subscriber.py
TEMPERATURE_THRESHOLD and ALARM_DURATION in subscriber.py

Notes

This implementation simulates temperature data. For a real-world scenario, replace the simulate_temperature() function in publisher.py with actual sensor readings.
The system uses a local MQTT broker. For cloud deployment, update the MQTT_BROKER address accordingly.
