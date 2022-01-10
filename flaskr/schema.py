from marshmallow import fields

from flaskr import ma


class UserSchemaForProfile(ma.Schema):
    id = fields.Integer()
    email = fields.Email()
    is_verified = fields.Boolean()
    role = fields.String()


class ProfileSchemaForPostCommentReply(ma.Schema):
    id = fields.Integer()
    first_name = fields.String()
    last_name = fields.String()
    profile_photo = fields.String()
    user = fields.Nested(UserSchemaForProfile)


class EventSchemaForPost(ma.Schema):
    id = fields.Integer()
    title = fields.String()


class ReplySchema(ma.Schema):
    id = fields.Integer()
    content = fields.String()
    profile = fields.Nested(ProfileSchemaForPostCommentReply)
    created_at = fields.DateTime()


class CommentSchema(ma.Schema):
    id = fields.Integer()
    content = fields.String()
    replies = fields.List(fields.Nested(ReplySchema))
    profile = fields.Nested(ProfileSchemaForPostCommentReply)
    post_id = fields.Integer()
    created_at = fields.DateTime()


class PostSchema(ma.Schema):
    id = fields.Integer()
    content = fields.String()
    up_vote = fields.List(fields.Integer())
    down_vote = fields.List(fields.Integer())
    comments = fields.List(fields.Nested(CommentSchema))
    created_at = fields.DateTime()
    profile = fields.Nested(ProfileSchemaForPostCommentReply)
    event = fields.Nested(EventSchemaForPost)


post_schema = PostSchema()
post_schemas = PostSchema(many=True)

comment_schema = CommentSchema()
comment_schemas = CommentSchema(many=True)

reply_schema = ReplySchema()
reply_schemas = ReplySchema(many=True)
