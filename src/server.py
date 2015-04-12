import redis
import argparse
from flask import Flask
app = Flask(__name__)

strict_redis = None

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--db", type=int, required=True)

    args = parser.parse_args()
    host = args.host
    port = args.port
    db = args.db
    strict_redis = redis.StrictRedis(host=host, port=port, db=db)
    app.run()
