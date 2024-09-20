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
