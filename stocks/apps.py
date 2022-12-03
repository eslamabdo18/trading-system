from django.apps import AppConfig
from threading import Thread


class StocksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stocks'

    def ready(self):
        print("22222")
        from .mqtt import Mqttclient
        Mqttclient().run()
        # mqtt.client.loop_start()
