FROM python:3.9

COPY main.py /app/main.py

RUN pip install paho-mqtt

RUN pip install json

WORKDIR /app

CMD ["python3", "main.py"]
