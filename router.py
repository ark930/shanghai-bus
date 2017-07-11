from flask import Flask
from flask import request
from bus import Bus
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'


@app.route('/bus/<router_name>/stop/<stop_id>')
def query_stop(router_name, stop_id):
    direction = request.args.get('direction', '0')

    bus = Bus()
    res = bus.query_stop(router_name, direction, stop_id)

    return json.dumps(res)


@app.route('/bus/<router_name>')
def query_router(router_name):
    direction = request.args.get('direction', '0')

    bus = Bus()
    routers = bus.query_router(router_name, direction)
    print(routers)

    return json.dumps(routers)

