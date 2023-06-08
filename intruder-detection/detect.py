from ultralytics import YOLO
from ultralytics.yolo.engine.results import Results
import numpy as np

model = YOLO(model="yolov8n.pt")


def detect(source: np.ndarray):
    results: Results = model.predict(
        source, save=False, stream=False, classes=[0], verbose=False
    )
    boxes = []
    for result in results:
        if result is None:
            continue
        if result.boxes is None:
            continue
        for box in result.boxes:
            boxes.append(box.xyxy.tolist()[0])
    return boxes
