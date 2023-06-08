# ---------------------------------------------------------------------------- #
# Description:                                                                 #
# This file contains a program that subscribes to a topic, receives images     #
# and detects intruders in the images.                                         #
# ---------------------------------------------------------------------------- #

print("Importing dependencies...")
import paho.mqtt.client as mqtt
from detect import detect
from args import args
from helpers import jpeg_bytes_to_numpy_array
import json

# ------------------------------ Callback Methods ----------------------------- #


# This method is called when the client receives a message from the broker
def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    # Read JPG and convert it to a numpy array
    image = jpeg_bytes_to_numpy_array(msg.payload)

    # Get the bounding boxes of the detected people
    boxes = detect(image)

    # Publish the bounding boxes
    client.publish(args.boxes_topic, json.dumps(boxes))


# ----------------------------------- Main ----------------------------------- #

if __name__ == "__main__":
    # Create a client
    client = mqtt.Client()

    # Set the callback method
    client.on_message = on_message

    # Connect to the broker
    print("Connecting to broker...")
    client.connect(args.broker_url, args.broker_port, 60)

    # Subscribe to the topic
    client.subscribe(args.image_topic)

    # Start the loop
    print("Listening for messages...")
    client.loop_forever()
