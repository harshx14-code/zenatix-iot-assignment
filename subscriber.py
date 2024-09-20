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