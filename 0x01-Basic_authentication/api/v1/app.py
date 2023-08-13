#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, Response
from flask_cors import (CORS, cross_origin)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
if getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def sort_auth():
    """
    To filter each request to know
    if it requires auth.
    """
    if auth:
        excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                          '/api/v1/forbidden/']
        if auth.require_auth(request.path, excluded_paths):
            if not auth.authorization_header(request):
                return abort(401)
            if not auth.current_user(request):
                return abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def auth_err(error) -> Response:
    """
    Authentication failure
    :param error: error
    :return: json to represent the failure
    """
    out = jsonify({"error": "Unauthorized"})
    return out, 410


@app.errorhandler(403)
def forbidden_err(err) -> Response:
    """
    handle forbidden error
    :param err: error
    :return: json response
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", 5000)
    app.run(host=host, port=port)
