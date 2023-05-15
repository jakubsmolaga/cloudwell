# Import the libraries
import torch
from PIL import Image
import cv2


# The detector class
class Detector:
    def __init__(self):
        self.model = torch.hub.load("ultralytics/yolov5", "yolov5n", pretrained=True)

    def __draw_warning(self, frame):
        bg_pos = (0, int(frame.shape[0] * 0.9))
        bg_size = (int(frame.shape[1] * 0.5), frame.shape[0])
        text = "Uwaga! Intruz!"
        text_pos = (0, int(frame.shape[0] * 0.95))
        text_font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.rectangle(frame, bg_pos, bg_size, (0, 0, 0), -1)
        cv2.putText(frame, text, text_pos, text_font, 1, (0, 0, 255), 2)

    def __find_people(self, frame):
        image = Image.fromarray(frame)
        results = self.model(image)
        results.xyxy[0] = results.xyxy[0][results.xyxy[0][:, 5] == 0]  # Get only people
        boxes = results.xyxy[0].detach().numpy()
        return boxes

    def __draw_boxes(self, frame, boxes):
        for box in boxes:
            pos = (int(box[0]), int(box[1]))
            size = (int(box[2]), int(box[3]))
            cv2.rectangle(frame, pos, size, (0, 0, 255), 2)

    def run(self, frame):
        boxes = self.__find_people(frame)
        if len(boxes) > 0:
            self.__draw_warning(frame)
        self.__draw_boxes(frame, boxes)
