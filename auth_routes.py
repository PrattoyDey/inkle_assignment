from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, User

# Create blueprint
auth_bp = Blueprint("auth", __name__)

# ---------- TEST ROUTE (IMPORTANT FOR YOUR 404 ISSUE) ----------
@auth_bp.get("/ping")
def ping():
    return jsonify({"message": "auth blueprint is working"}), 200


# ---------- SIGNUP ROUTE ----------
@auth_bp.post("/signup")
def signup():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Missing fields
    if not all([name, email, password]):
        return jsonify({"message": "name, email, password are required"}), 400

    # Duplicate email
    existing = User.query.filter_by(email=email).first()
    if existing:
        return jsonify({"message": "Email already registered"}), 400

    # Create user
    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role="user",
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


# ---------- LOGIN ROUTE ----------
@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    # Missing fields
    if not all([email, password]):
        return jsonify({"message": "email and password are required"}), 400

    # Find user
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401

    # Create JWT
    access_token = create_access_token(
        identity={"id": user.id, "role": user.role}
    )

    return jsonify(
        {
            "access_token": access_token,
            "user": user.to_dict(),
        }
    ), 200