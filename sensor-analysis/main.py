import paho.mqtt.client as mqtt
import json

# Konfiguracja danych MQTT
mqtt_broker = "mqtt-broker"
mqtt_port = 1883
mqtt_topic_temp = "temperature"
mqtt_topic_hum = "humidity"
mqtt_topic_alarm = "alarm"

# Stałe określające progi temperatury i wilgotności
temp_min = 15
temp_max = 30
hum_min = 40
hum_max = 60

# Funkcja wywoływana po podłączeniu do brokera MQTT
def on_connect(client, userdata, flags, rc):
    print("Połączono z MQTT brokerem. Kod: " + str(rc))
    client.subscribe(mqtt_topic_temp)
    client.subscribe(mqtt_topic_hum)

# Funkcja wywoływana po wysłaniu wiadomości MQTT
def on_publish(client, userdata, mid):
    print("Wysłano wiadomość")

# Funkcja wywoływana po otrzymaniu wiadomości MQTT
def on_message(client, userdata, msg):
    data = {
                "property_id": 1,
                "alarm_type": "abc",
                "current_val": 0,
                "alarm_val": 0
    }
    if msg.topic == mqtt_topic_temp:
        temp = msg.payload.decode("utf-8")
        temp = float(temp)
        data["current_val"] = temp
        if temp < temp_min:
            print("Temperatura jest zbyt niska!")
            data["alarm_type"] = "min_temp"
            data["alarm_val"] = temp_min
            json_data = json.dumps(data)
            client.publish(mqtt_topic_alarm, json_data)
        elif temp > temp_max:
            print("Temperatura jest zbyt wysoka!")
            data["alarm_type"] = "max_temp"
            data["alarm_val"] = temp_max
            json_data = json.dumps(data)
            client.publish(mqtt_topic_alarm, json_data)
            print(data)
    if msg.topic == mqtt_topic_hum:
        hum = msg.payload.decode("utf-8")
        hum = float(temp)

        if hum < hum_min:
            print("Wilgotność jest zbyt niska!")
            data["alarm_type"] = "min_hum"
            data["alarm_val"] = hum_min
            json_data = json.dumps(data)
            client.publish(mqtt_topic_alarm, json_data)
        elif hum > hum_max:
            print("Wilgotność jest zbyt wysoka!")
            data["alarm_type"] = "max_hum"
            data["alarm_val"] = hum_max
            json_data = json.dumps(data)
            client.publish(mqtt_topic_alarm, json_data)

# Inicjalizacja klienta MQTT
client = mqtt.Client()
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message

# Podłączenie do brokera MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Uruchomienie pętli klienta MQTT
client.loop_forever()
