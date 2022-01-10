from flask import Blueprint, flash, jsonify, request
from flask_login import current_user, login_required
from flaskr import app, db
from flaskr.api.utils import get_user
from flaskr.decorators import is_token_verified
from flaskr.models import Comment, Event, Post, Profile, Reply, User
from flaskr.schema import (comment_schema, comment_schemas, post_schema,
                           post_schemas, reply_schema, reply_schemas)

posts = Blueprint("posts", __name__, url_prefix="/api/v1/posts")


@posts.route("", methods=["POST"])
@is_token_verified
def create():
    content = request.json.get("content")
    profile_id = request.json.get("profile_id")
    event_id = request.json.get("event_id")

    profile = Profile.query.get(profile_id)
    event = Event.query.get(event_id)

    if not content or not event_id or not profile:
        return jsonify({
            "error": "Request data is not valid. Some field is missing."
        }), 400

    if profile.id not in event.members and profile.id != event.host.id:
        return jsonify({
            "error": "Only members or host can post in this event."
        }), 401

    post = Post(content, None, profile.id, event.id)

    db.session.add(post)
    db.session.commit()

    return post_schema.jsonify(post), 201


@posts.route("/up-vote/<int:id>", methods=["PATCH"])
@is_token_verified
def up_vote(id: int):
    profile_id = request.json.get("profile_id")
    profile = User.query.get(profile_id).profile

    post = Post.query.get(id)
    if not profile or not post:
        return jsonify({
            "error": "Profile or post not found."
        }), 404
    if profile.id in post.up_vote:
        post.remove_up_vote(profile.id)
    else:
        post.add_up_vote(profile.id)
    if profile.id in post.down_vote:
        post.remove_down_vote(profile.id)
    return post_schema.jsonify(post), 200


@posts.route("/down-vote/<int:id>", methods=["PATCH"])
@is_token_verified
def down_vote(id: int):
    profile_id = request.json.get("profile_id")
    profile = User.query.get(profile_id).profile

    post = Post.query.get(id)
    if not profile or not post:
        return jsonify({
            "error": "Profile or post not found."
        }), 404

    if profile.id in post.down_vote:
        post.remove_down_vote(profile.id)
    else:
        post.add_down_vote(profile.id)
    if profile.id in post.up_vote:
        post.remove_up_vote(profile.id)
    return post_schema.jsonify(post), 200


@posts.route("/<int:id>", methods=["DELETE"])
@is_token_verified
def delete(id: int):
    user_id = get_user()
    profile = User.query.get(user_id).profile
    post = Post.query.get(int(id))
    if not profile or not post:
        return jsonify({
            "error": "Profile or post not found."
        }), 404
    if profile.id != post.profile.id:
        return jsonify({
            "error": "You can't delete this post."
        }), 406
    db.session.delete(post)
    db.session.commit()

    return jsonify({
        "message": "Successfully deleted the post"
    }), 200
