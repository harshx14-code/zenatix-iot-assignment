# zenatix-iot-assignment

Problem Statement

 
Consider an IoT device that reads data from the southbound sensors, and publishes them to the cloud.

 
The IoT device is installed in a branch of a renowned hotel chain, where customer's leisure and comfort are given utmost importance. The Manager of the hotel wants a solution where your IoT device interfaces with an on-premise temperature sensor and raises an alarm to the Manager, whenever the temperature crosses a certain threshold for a certain duration. This would ensure the maintenance of an optimal room temperature, and hence the customers' comfort

Goals:

Publisher Program
import paho.mqtt.client as mqtt
import random
import time
from datetime import datetime

broker = 'broker.hivemq.com'
port = 1883
topic = "hotel/temperature"
client = mqtt.Client()

def connect_mqtt():
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        temperature = round(random.uniform(18.0, 30.0), 2)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payload = f"{temperature},{timestamp}"
        client.publish(topic, payload)
        print(f"Published {payload}")
        time.sleep(60)

if __name__ == '__main__':
    client = connect_mqtt()
    client.loop_start()
    publish(client)


 
Each data point should be read after every 60-second delay and published to the cloud (MQTT Broker). (working)

 
Subscriber Program
import paho.mqtt.client as mqtt
import csv
import re

broker = 'broker.hivemq.com'
port = 1883
topic = "hotel/temperature"
threshold = 25.0
alarm_duration = 5
temp_list = []

def clean_temperature(temp_str):
    # Remove all characters except digits, dots, and minus sign
    cleaned = re.sub(r'[^\d.-]', '', temp_str)
    # Ensure there's only one dot for decimal point
    parts = cleaned.split('.')
    if len(parts) > 2:
        cleaned = parts[0] + '.' + ''.join(parts[1:])
    return cleaned

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    temperature_str, timestamp = data.split(',')
    
    cleaned_temp_str = clean_temperature(temperature_str)
    try:
        temperature = float(cleaned_temp_str)
    except ValueError:
        print(f"Invalid temperature value: {temperature_str}")
        return

    temp_list.append((temperature, timestamp))
    if len(temp_list) > alarm_duration:
        temp_list.pop(0)
    
    if all(temp[0] > threshold for temp in temp_list):
        print("ALARM: Temperature too high for 5 minutes!")
    
    with open('temperature_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([temperature, timestamp])
    
    print(f"Logged {temperature} at {timestamp}")

client = mqtt.Client()
client.connect(broker, port)
client.subscribe(topic)
client.on_message = on_message
client.loop_forever()

 
It should raise an alarm every time a sensor crosses a certain threshold continuously for 5 minutes (i.e. 5 data points). (working)

 
The data points should be saved locally for every sensor, with respective timestamps.

 
Server Program
from flask import Flask, jsonify
import csv

app = Flask(__name__)

def get_last_temperature():
    try:
        with open('temperature_data.csv', 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                last_row = rows[-1]
                return {'temperature': last_row[0], 'timestamp': last_row[1]}
            else:
                return {'error': 'No data available'}
    except FileNotFoundError:
        return {'error': 'Temperature data file not found'}

@app.route('/temperature', methods=['GET'])
def latest_temperature():
    last_temp = get_last_temperature()
    return jsonify(last_temp)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Temperature Server. Use /temperature to get the latest temperature."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 
An HTTP server exposing the sensor data should return the last value for the sensors when an API call is made to the server. (You can use web application frameworks like Flask, FastAPI, etc.) (working)

Now open cmd prompt type python publisher.py it will start taking temperature after every 60 sec
Verify the publisher is generating random temperature values every 60 seconds and sending them to the broker. if yes good to go

Now open cmd prompt type python subscriber.py it will Confirm the subscriber is receiving data, saving it in temperature_data.csv, and raising an alarm if the temperature exceeds the threshold for 5 consecutive readings.

BUT save the publisher.py and subscriber.py and server.py in the samne directory in cmd

now type python server.py it will give ouput http://127.0.0.1:5000/

Now that the server is running, you can use a web browser or a tool like curl or Postman to make HTTP requests to your server. i checked with postman desktop agent.
press ctrl+c  to stop 
 

hence the problem of the hotel manager is solved by following above mentioned steps
