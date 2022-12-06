import json
import uuid
import paho.mqtt.client as mqtt
# from .services import StockService
import random


MQTT_HOST = "vernemq"
MQTT_PORT = 1883
MQTT_TOPIC = "thndr-trading"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    __instance = None

    # print(__instance)

    def __new__(cls, *args, **kwargs):
        print(cls.__instance)
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance


class Mqttclient():

    def __init__(self):
        print("hereeeee")
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(
            host=MQTT_HOST,
            port=MQTT_PORT,
            keepalive=60
        )

    def on_connect(self, mqtt_client, userdata, flags, rc):
        if rc == 0:
            print('Connected successfully')
            mqtt_client.connected_flag = True
            mqtt_client.subscribe("thndr-trading")
        else:
            print('Bad connection. Code:', rc)

    def on_message(self, mqtt_client, userdata, msg):

        from .services import StockService
        from trade.order_matcher import OrderMatcher

        stock = json.loads(msg.payload)
        # 1 means buy opeartion
        OrderMatcher.confirm_operation(stock, 1)
        # 2 means sell operation
        OrderMatcher.confirm_operation(stock, 2)
        # insert the current stock into db
        StockService.update_stock_db(stock)

    def run(self):
        self.client.loop_start()
