import paho.mqtt.client as mqtt
import redis

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test/topic")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    r.set(msg.topic, msg.payload)

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt-broker", 1883, 60)

client.loop_forever()