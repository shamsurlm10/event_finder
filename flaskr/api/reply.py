from flask import Blueprint, request
from flask.json import jsonify
from flaskr import db
from flaskr.api.utils import get_user
from flaskr.decorators import is_token_verified
from flaskr.models import Comment, Post, Profile, Reply, User
from flaskr.schema import (comment_schema, comment_schemas, post_schema,
                           post_schemas, reply_schema, reply_schemas)

replies = Blueprint("replies", __name__, url_prefix="/api/v1/replies")

@replies.route("", methods=["POST"])
@is_token_verified
def create():
    content = request.json.get("content")
    profile_id = request.json.get("profile_id")
    comment_id = request.json.get("comment_id")

    profile = Profile.query.get(profile_id)
    comment = Comment.query.get(comment_id)
    
    if not content or not comment or not profile:
        return jsonify({
            "error": "Request data is not valid. Some field is missing."
        }), 400
    
    reply = Reply(content, comment.id, profile.id)

    db.session.add(reply)
    db.session.commit()

    return reply_schema.jsonify(reply), 201


@replies.route("", methods=["GET"])
def get_all():
    pass


@replies.route("/<int:id>", methods=["GET"])
def get(id: int):
    pass


@replies.route("/<int:id>", methods=["PUT"])
def update(id: int):
    pass


@replies.route("/<int:id>", methods=["DELETE"])
@is_token_verified
def delete(id: int):
    user_id = get_user()
    profile = User.query.get(user_id).profile
    reply = Reply.query.get(int(id))
    if not profile or not reply:
        return jsonify({
            "error": "Profile or reply not found."
        }), 404
    if profile.id!=reply.profile.id:
        return jsonify({
            "error": "You can't delete this reply."
        }), 406
    db.session.delete(reply)
    db.session.commit()
    
    return jsonify({
        "message": "Successfully deleted the reply"
        }), 200
