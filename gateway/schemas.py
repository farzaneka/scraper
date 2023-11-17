from marshmallow import Schema, fields


class CreateFeedSchema(Schema):
    id = fields.Str(required=True)
    member_id = fields.Int(required=True)
    url = fields.Str(required=True)


class ProductSchema(Schema):
    id = fields.Str(required=True)
    title = fields.Str(required=True)
    maximum_speed = fields.Int(required=True)
    in_stock = fields.Int(required=True)
    passenger_capacity = fields.Int(required=True)

