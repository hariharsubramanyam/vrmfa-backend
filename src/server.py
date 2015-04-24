import build_museum
import argparse
from flask import Flask, Response
app = Flask(__name__)

dbname = None
user = None
host = None
port = None
db = None

@app.route("/")
def museum():
    museum_rooms = build_museum.build_museum(dbname, user, host, port, db)
    json_str = build_museum.rooms_to_json(museum_rooms)
    return Response(response=json_str, status=200, mimetype="application/json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbname", type=str, required=True)
    parser.add_argument("--user", type=str, required=True)
    parser.add_argument("--host", type=str, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--db", type=int, required=True)

    args = parser.parse_args()
    dbname = args.dbname
    user = args.user
    host = args.host
    port = args.port
    db = args.db
    app.run(host='0.0.0.0', port=8000)
