# ---------------------------------------------------------------------------- #
# Description: This file contains the arguments for the intruder detection     #
#              system.                                                         #
# ---------------------------------------------------------------------------- #

import os
from attr import dataclass

# Define defaults
DEFAULT_BROKER_URL = "localhost"
DEFAULT_BROKER_PORT = 1883
DEFAULT_IMAGE_TOPIC = "image"
DEFAULT_BOXES_TOPIC = "boxes"
DEFAULT_ALARM_TOPIC = "alarms"


# Define a typed data class that holds the arguments
@dataclass
class Args:
    broker_url: str
    broker_port: int
    image_topic: str
    boxes_topic: str
    alarm_topic: str


# Create an instance of the data class
args = Args(
    broker_url=os.environ.get("BROKER_URL", DEFAULT_BROKER_URL),
    broker_port=int(os.environ.get("BROKER_PORT", DEFAULT_BROKER_PORT)),
    image_topic=os.environ.get("IMAGE_TOPIC", DEFAULT_IMAGE_TOPIC),
    boxes_topic=os.environ.get("BOXES_TOPIC", DEFAULT_BOXES_TOPIC),
    alarm_topic=os.environ.get("ALARM_TOPIC", DEFAULT_ALARM_TOPIC),
)
