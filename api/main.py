import flask
from influxdb_client import InfluxDBClient

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
    res = res[0]
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
