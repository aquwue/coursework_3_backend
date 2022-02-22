from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)
    password = fields.Str(load_only=True)
    name = fields.Str(required=True)
    surname = fields.Str()
    favorite_genre = fields.Str()
