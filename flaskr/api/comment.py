from flask import Blueprint, flash, request
from flask.json import jsonify
from flaskr import db
from flaskr.decorators import is_token_verified
from flaskr.models import Comment, Post, Profile, Reply, User
from flaskr.schema import (comment_schema, comment_schemas, post_schema,
                           post_schemas, reply_schema, reply_schemas)
from flaskr.api.utils import get_user

comments = Blueprint("comment", __name__, url_prefix="/api/v1/comments")

@comments.route("", methods=["POST"])
@is_token_verified
def create():
    content = request.json.get("content")
    profile_id = request.json.get("profile_id")
    post_id = request.json.get("post_id")

    profile = Profile.query.get(profile_id)
    post = Post.query.get(post_id)
    
    if not content or not post_id or not profile:
        return jsonify({
            "error": "Request data is not valid. Some field is missing."
        }), 400
    
    comment = Comment(content, post.id, profile.id)

    db.session.add(comment)
    db.session.commit()

    return comment_schema.jsonify(comment), 201


@comments.route("", methods=["GET"])
def get_all():
    pass


@comments.route("/<int:id>", methods=["GET"])
def get(id: int):
    pass


@comments.route("/<int:id>", methods=["PUT"])
def update(id: int):
    pass


@comments.route("/<int:id>", methods=["DELETE"])
@is_token_verified
def delete(id: int):
    user_id = get_user()
    profile = User.query.get(user_id).profile
    comment = Comment.query.get(int(id))
    if not profile or not comment:
        return jsonify({
            "error": "Profile or comment not found."
        }), 404
    if profile.id!=comment.profile.id:
        return jsonify({
            "error": "You can't delete this comment."
        }), 406
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({
        "message": "Successfully deleted the comment"
        }), 200
