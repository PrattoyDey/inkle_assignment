from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import db, Post, Like, Block, Activity, User
from helpers import get_current_user, role_required

post_bp = Blueprint("posts", __name__)


@post_bp.post("/")
@jwt_required()
def create_post():
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    data = request.get_json() or {}
    content = data.get("content")
    if not content:
        return jsonify({"message": "content is required"}), 400

    post = Post(content=content, author_id=current.id)
    db.session.add(post)

    # Activity: "ABC made a post"
    activity_text = f"{current.name} made a post"
    activity = Activity(text=activity_text, type="post")
    db.session.add(activity)

    db.session.commit()
    return jsonify({"message": "Post created", "post": post.to_dict()}), 201


@post_bp.get("/")
@jwt_required()
def list_posts():
    """
    Get all posts that the current user is allowed to see.
    If A blocks B -> B should not be able to see posts from A.
    So if current user is B, we hide posts whose author has blocked B.
    """
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    # Find all users who have blocked this current user
    blocked_by = Block.query.filter_by(blocked_id=current.id).all()
    blocked_by_ids = {b.blocker_id for b in blocked_by}

    posts = Post.query.order_by(Post.created_at.desc()).all()
    visible_posts = [
        p.to_dict() for p in posts if p.author_id not in blocked_by_ids
    ]

    return jsonify(visible_posts), 200


@post_bp.delete("/<int:post_id>")
@role_required(["admin", "owner"])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404

    # Delete likes on this post
    Like.query.filter_by(post_id=post.id).delete()

    db.session.delete(post)

    # Activity: "Post deleted by Admin/Owner"
    current = get_current_user()
    role = current.role if current else "admin"
    if role == "owner":
        activity_text = "Post deleted by Owner"
    else:
        activity_text = "Post deleted by Admin"

    activity = Activity(text=activity_text, type="delete_post")
    db.session.add(activity)

    db.session.commit()
    return jsonify({"message": "Post deleted"}), 200


@post_bp.post("/<int:post_id>/like")
@jwt_required()
def like_post(post_id):
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"message": "Post not found"}), 404

    # Check if the post's author has blocked current user
    block = Block.query.filter_by(
        blocker_id=post.author_id, blocked_id=current.id
    ).first()
    if block:
        return jsonify({"message": "You are blocked by this user"}), 403

    existing = Like.query.filter_by(
        user_id=current.id, post_id=post_id
    ).first()
    if existing:
        return jsonify({"message": "Already liked"}), 400

    like = Like(user_id=current.id, post_id=post_id)
    db.session.add(like)

    # Activity: "PQR liked ABC's post"
    author = User.query.get(post.author_id)
    activity_text = f"{current.name} liked {author.name}'s post"
    activity = Activity(text=activity_text, type="like")
    db.session.add(activity)

    db.session.commit()
    return jsonify({"message": "Post liked"}), 201


@post_bp.post("/<int:post_id>/unlike")
@jwt_required()
def unlike_post(post_id):
    current = get_current_user()
    if not current:
        return jsonify({"message": "Current user not found"}), 404

    like = Like.query.filter_by(
        user_id=current.id, post_id=post_id
    ).first()
    if not like:
        return jsonify({"message": "Not liked"}), 400

    db.session.delete(like)
    db.session.commit()
    return jsonify({"message": "Post unliked"}), 200