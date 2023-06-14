import paho.mqtt.client as mqtt
import json

# Konfiguracja danych MQTT
mqtt_broker = "mqtt-broker"
mqtt_port = 1883
mqtt_topic_temp = "temperature"
mqtt_topic_hum = "humidity"
mqtt_topic_alarm = "alarms"
mqtt_topic_settings = "settings"

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
    client.subscribe(mqtt_topic_settings)

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
        hum = float(hum)
        data["current_val"] = hum
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


# Funkcja wywoływana po otrzymaniu wiadomości o ustawieniach
def on_settings_message(client, userdata, msg):
    global temp_min, temp_max, hum_min, hum_max
    settings = json.loads(msg.payload)
    print("Ustawienia alarmów zostały zaktualizowane:", settings)
    temp_min = float(settings.get("min_temp", temp_min))
    temp_max = float(settings.get("max_temp", temp_max))
    hum_min = float(settings.get("min_hum", hum_min))
    hum_max = float(settings.get("max_hum", hum_max))
    


# Inicjalizacja klienta MQTT
client = mqtt.Client()
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message
client.message_callback_add(mqtt_topic_settings, on_settings_message)

# Podłączenie do brokera MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Uruchomienie pętli klienta MQTT
client.loop_forever()
