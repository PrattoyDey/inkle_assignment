from flask import Blueprint, jsonify
from flask import request
from flask_jwt_extended import jwt_required

from models import db, User, Follow, Block, Activity, Post, Like
from helpers import role_required, get_current_user

user_bp = Blueprint("users", __name__)


@user_bp.get("/me")
@jwt_required()
def me():
    user = get_current_user()
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@user_bp.get("/")
@jwt_required()
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@user_bp.post("/follow/<int:target_id>")
@jwt_required()
def follow_user(target_id):
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    if current.id == target_id:
        return jsonify({"message": "Cannot follow yourself"}), 400

    target = User.query.get(target_id)
    if not target:
        return jsonify({"message": "Target user not found"}), 404

    existing = Follow.query.filter_by(
        follower_id=current.id, followee_id=target_id
    ).first()
    if existing:
        return jsonify({"message": "Already following"}), 400

    follow = Follow(follower_id=current.id, followee_id=target_id)
    db.session.add(follow)

    # Activity: "X followed Y"
    activity_text = f"{current.name} followed {target.name}"
    activity = Activity(text=activity_text, type="follow")
    db.session.add(activity)

    db.session.commit()
    return jsonify({"message": "Followed successfully"}), 201


@user_bp.post("/unfollow/<int:target_id>")
@jwt_required()
def unfollow_user(target_id):
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    follow = Follow.query.filter_by(
        follower_id=current.id, followee_id=target_id
    ).first()
    if not follow:
        return jsonify({"message": "Not following"}), 400

    db.session.delete(follow)
    db.session.commit()
    return jsonify({"message": "Unfollowed successfully"}), 200


@user_bp.post("/block/<int:blocked_id>")
@jwt_required()
def block_user(blocked_id):
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    if current.id == blocked_id:
        return jsonify({"message": "Cannot block yourself"}), 400

    target = User.query.get(blocked_id)
    if not target:
        return jsonify({"message": "User to block not found"}), 404

    existing = Block.query.filter_by(
        blocker_id=current.id, blocked_id=blocked_id
    ).first()
    if existing:
        return jsonify({"message": "Already blocked"}), 400

    block = Block(blocker_id=current.id, blocked_id=blocked_id)
    db.session.add(block)

    # Also unfollow if following
    Follow.query.filter_by(
        follower_id=current.id, followee_id=blocked_id
    ).delete()

    db.session.commit()
    return jsonify({"message": "User blocked"}), 201


@user_bp.post("/unblock/<int:blocked_id>")
@jwt_required()
def unblock_user(blocked_id):
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    block = Block.query.filter_by(
        blocker_id=current.id, blocked_id=blocked_id
    ).first()
    if not block:
        return jsonify({"message": "Not blocked"}), 400

    db.session.delete(block)
    db.session.commit()
    return jsonify({"message": "User unblocked"}), 200


# -------- ADMIN / OWNER ACTIONS --------


@user_bp.delete("/<int:user_id>")
@role_required(["admin", "owner"])
def delete_user(user_id):
    # Admin or Owner can delete user
    target = User.query.get(user_id)
    if not target:
        return jsonify({"message": "User not found"}), 404

    # Cascade delete:
    Like.query.filter_by(user_id=target.id).delete()
    Follow.query.filter_by(follower_id=target.id).delete()
    Follow.query.filter_by(followee_id=target.id).delete()
    Block.query.filter_by(blocker_id=target.id).delete()
    Block.query.filter_by(blocked_id=target.id).delete()

    # Delete user's posts and associated likes
    posts = Post.query.filter_by(author_id=target.id).all()
    for p in posts:
        Like.query.filter_by(post_id=p.id).delete()
        db.session.delete(p)

    db.session.delete(target)

    # Log activity
    # Who is doing this? Current user from JWT
    current = get_current_user()
    role = current.role if current else "admin"
    if role == "owner":
        activity_text = "User deleted by Owner"
    else:
        activity_text = "User deleted by Admin"

    activity = Activity(text=activity_text, type="delete_user")
    db.session.add(activity)

    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200


@user_bp.post("/make-admin/<int:user_id>")
@role_required(["owner"])
def make_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.role = "admin"
    db.session.commit()
    return jsonify({"message": "User promoted to admin"}), 200


@user_bp.post("/remove-admin/<int:user_id>")
@role_required(["owner"])
def remove_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.role != "admin":
        return jsonify({"message": "User is not an admin"}), 400

    user.role = "user"
    db.session.commit()
    return jsonify({"message": "Admin role removed"}), 200