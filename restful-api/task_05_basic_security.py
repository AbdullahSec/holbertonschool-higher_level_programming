#!/usr/bin/python3
"""Protect Flask API endpoints with Basic Auth and JWT roles."""

import os
import secrets
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY", secrets.token_hex(32)
)
jwt = JWTManager(app)
auth = HTTPBasicAuth()

users = {
    "user1": {
        "username": "user1",
        "password": generate_password_hash("password"),
        "role": "user",
    },
    "admin1": {
        "username": "admin1",
        "password": generate_password_hash("password"),
        "role": "admin",
    },
}


@auth.verify_password
def verify_password(username, password):
    """Verify a Basic Auth password against its stored hash."""
    user = users.get(username)
    if user and check_password_hash(user["password"], password or ""):
        return username
    return None


@auth.error_handler
def basic_auth_error(_status):
    """Return a consistent response for Basic Auth failures."""
    return jsonify({"error": "Unauthorized"}), 401


@jwt.unauthorized_loader
def missing_token_error(_reason):
    """Return 401 when a protected route has no token."""
    return jsonify({"error": "Missing or invalid token"}), 401


@jwt.invalid_token_loader
def invalid_token_error(_reason):
    """Return 401 when a token is malformed or invalid."""
    return jsonify({"error": "Invalid token"}), 401


@jwt.expired_token_loader
def expired_token_error(_header, _payload):
    """Return 401 when a token has expired."""
    return jsonify({"error": "Token has expired"}), 401


@jwt.revoked_token_loader
def revoked_token_error(_header, _payload):
    """Return 401 when a token has been revoked."""
    return jsonify({"error": "Token has been revoked"}), 401


@jwt.needs_fresh_token_loader
def fresh_token_error(_header, _payload):
    """Return 401 when a fresh token is required."""
    return jsonify({"error": "Fresh token required"}), 401


@app.route("/basic-protected")
@auth.login_required
def basic_protected():
    """Return a message after successful Basic Auth."""
    return "Basic Auth: Access Granted"


@app.route("/login", methods=["POST"])
def login():
    """Validate user credentials and return a JWT access token."""
    credentials = request.get_json(silent=True)
    if not isinstance(credentials, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    username = credentials.get("username")
    password = credentials.get("password")
    user = users.get(username)
    if not user or not check_password_hash(user["password"], password or ""):
        return jsonify({"error": "Bad username or password"}), 401

    token = create_access_token(
        identity=username, additional_claims={"role": user["role"]}
    )
    return jsonify({"access_token": token})


@app.route("/jwt-protected")
@jwt_required()
def jwt_protected():
    """Return a message after successful JWT authentication."""
    get_jwt_identity()
    return "JWT Auth: Access Granted"


@app.route("/admin-only")
@jwt_required()
def admin_only():
    """Allow only users whose JWT role is admin."""
    if get_jwt().get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return "Admin Access: Granted"


if __name__ == "__main__":
    app.run()
