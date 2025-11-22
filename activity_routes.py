from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from models import Activity

activity_bp = Blueprint("activity", __name__)


@activity_bp.get("/")
@jwt_required()
def get_activity_feed():
    activities = Activity.query.order_by(
        Activity.created_at.desc()
    ).limit(50).all()

    return jsonify([a.to_dict() for a in activities]), 200