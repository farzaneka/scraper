from marshmallow import Schema, fields


class FeedSchema(Schema):
    id = fields.Int(required=True)
    member_id = fields.Int(required=True)
    url = fields.Str(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class BookmarkSchema(Schema):
    id = fields.Int(required=True)
    member_id = fields.Int(required=True)
    feed_item_id = fields.Int(required=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

