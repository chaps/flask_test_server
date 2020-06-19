from flask import request
from flask import Flask

import flask
import time
app = Flask(__name__)


app.routes = {}

@app.route('/', defaults={'path_string': ''})
@app.route('/<path:path_string>')
def mock_responses(path_string):
    path_string = "/" + path_string
    if path_string not in app.routes:
        # Return a 404 status code.
        return "", 404
    mock_info = app.routes[path_string]
    status_code = 200 if not "status_code" in mock_info else mock_info["status_code"]
    resp = flask.Response(mock_info["response"])
    if "headers" in mock_info:
        resp.headers = mock_info["headers"]
    if "delay" in mock_info:
        time.sleep(mock_info["delay"])
    return resp, status_code


@app.route('/register_routes', methods=["POST", "GET", "DELETE"])
def register_route():
    # Return all current routs
    if request.method == "GET":
        return app.routes
    # Will delete all routes
    if request.method == "DELETE":
        app.routes = {}
        return app.routes
    # Adds routes:
    payload = request.get_json(force=True)
    route = payload["route"]
    payload.pop("route")
    app.routes[route] = payload
    return app.routes





