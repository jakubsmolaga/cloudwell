import paho.mqtt.subscribe
import json
from args import args
from io import BytesIO
from PIL import Image
import threading

boxes = []


def image_callback(client, userdata, msg):
    b = BytesIO(msg.payload)
    image = Image.open(b, formats=["jpeg"])
    image.save("image.jpg")


def boxes_callback(client, userdata, msg):
    global boxes
    boxes = json.loads(msg.payload)
    print("New boxes:")
    print(boxes)


def __subscribe_image():
    paho.mqtt.subscribe.callback(
        image_callback,
        args.image_topic,
        hostname=args.broker_url,
        port=args.broker_port,
    )


def __subscribe_boxes():
    paho.mqtt.subscribe.callback(
        boxes_callback,
        args.boxes_topic,
        hostname=args.broker_url,
        port=args.broker_port,
    )


threading.Thread(target=__subscribe_image).start()
threading.Thread(target=__subscribe_boxes).start()
