import json

import paho.mqtt.client as mqtt
from .services import StockService


MQTT_HOST = "vernemq"
MQTT_PORT = 1883
MQTT_TOPIC = "thndr-trading"


def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe("thndr-trading")
    else:
        print('Bad connection. Code:', rc)


def on_message(mqtt_client, userdata, msg):
    stock = json.loads(msg.payload)
    StockService.update_stock_db(stock)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    host=MQTT_HOST,
    port=MQTT_PORT,
    keepalive=60
)
