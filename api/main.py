print("Importing dependencies...")
import flask
from influxdb_client import InfluxDBClient
import images
from args import args
import paho.mqtt.publish
import os

print("Imported dependencies!")

# Connect to InfluxDB
influx = InfluxDBClient(url="http://influxdb:8086", token="cloudwell", org="cloudwell")

# Check if InfluxDB is running
try:
    influx.health()
except:
    print("InfluxDB isn't running")
    exit(1)

# Create a read API client
query_api = influx.query_api()

# Create Flask app
app = flask.Flask(__name__)


# Index route
@app.route("/")
def hello():
    res = {"hello": "world"}
    return res


@app.route("/image")
def get_image():
    if not os.path.exists("image.jpg"):
        return flask.Response(status=404)
    return flask.send_file("image.jpg", mimetype="image/jpeg")


@app.route("/boxes")
def get_boxes():
    return flask.jsonify(images.boxes)


@app.route("/upload-image", methods=["POST"])
def upload_image():
    # Get image
    image = flask.request.files["image"]
    # Save image
    image.save("image.jpg")
    # Send image over mqtt
    with open("image.jpg", "rb") as f:
        image_bytes = f.read()
        paho.mqtt.publish.single(
            args.image_topic,
            image_bytes,
            hostname=args.broker_url,
            port=args.broker_port,
        )
    # Return success
    return flask.jsonify({"success": True})


# Get temperature
@app.route("/temperature")
def get_temperature():
    # Get last temperature
    query = 'from(bucket: "cloudwell") |> range(start: -1h) |> filter(fn: (r) => r._measurement == "temperature") |> last()'
    tables = query_api.query(query)
    # Convert data to JSON
    res = []
    for table in tables:
        for record in table.records:
            res.append({"time": record.get_time(), "value": record.get_value()})
    if len(res) == 0:
        return flask.Response(status=404)
    res = res[0]
    return flask.jsonify(res)


@app.route("/measurements")
def get_measurements():
    # Get last temperature
    query = 'from(bucket: "cloudwell") |> range(start: -24h) |> filter(fn: (r) => r._measurement == "temperature") |> last()'
    tables = query_api.query(query)
    # Convert data to JSON
    temperatures = []
    for table in tables:
        for record in table.records:
            temperatures.append(
                {"time": record.get_time(), "value": record.get_value()}
            )
    # Get last humidity
    query = 'from(bucket: "cloudwell") |> range(start: -24h) |> filter(fn: (r) => r._measurement == "humidity") |> last()'
    tables = query_api.query(query)
    # Convert data to JSON
    humidities = []
    for table in tables:
        for record in table.records:
            humidities.append({"time": record.get_time(), "value": record.get_value()})
    if len(temperatures) == 0 or len(humidities) == 0:
        return flask.Response(status=404)
    res = {"temperature": temperatures[0], "humidity": humidities[0]}
    return flask.jsonify(res)


# Setup CORS
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response


# Start Flask app
app.run(host="0.0.0.0", port=5000, debug=False)
