import redis
import flask

# Connect to Redis
r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

# Check if Redis is running
try:
    r.ping()
except redis.exceptions.ConnectionError:
    print("Redis isn't running")
    exit(1)

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
    res = {"temperature": r.get("temperature")}
    return res

# Setup CORS
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response

# Start Flask app
app.run(host="0.0.0.0", port=5000, debug=False)
