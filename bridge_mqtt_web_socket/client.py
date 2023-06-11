import paho.mqtt.client as mqtt
import asyncio
import websockets
import sys


log_file = open("log_client.txt", "a")
sys.stdout = log_file
sys.stderr = log_file

# Inicjalizacja klienta MQTT
mqtt_client = mqtt.Client()


# Klasa obsługująca klienta Web Socket
class WebSocketClient:
    def __init__(self, server_address):
        self.server_address = server_address
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.server_address)

    async def send_message(self, message):
        if self.websocket:
            await self.websocket.send(message)

    async def receive_message(self):
        if self.websocket:
            message = await self.websocket.recv()
            print("Otrzymano wiadomość Web Socket:", message)

    async def disconnect(self):
        if self.websocket:
            await self.websocket.close()


# Inicjalizacja klienta Web Socket
websocket_client = WebSocketClient("ws://127.0.0.1:8765")


# Funkcja obsługująca otrzymane wiadomości MQTT
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    print("Otrzymano wiadomość MQTT:", message)
    asyncio.run(websocket_client.send_message(message))


# Konfiguracja klienta MQTT
mqtt_broker = "mqtt-broker"
mqtt_topic = "alarms"
mqtt_client.on_message = on_message


# Funkcja obsługująca klienta MQTT
def mqtt_client_function():
    mqtt_client.connect(mqtt_broker)
    mqtt_client.subscribe(mqtt_topic)
    mqtt_client.loop_start()


# Funkcja obsługująca klienta Web Socket
async def websocket_client_function():
    await websocket_client.connect()
    while True:
        await websocket_client.receive_message()


# Funkcja główna
async def main():
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, mqtt_client_function)
    await websocket_client_function()


# Uruchomienie programu
try:
    asyncio.run(main())
finally:
    log_file.close()
