# from marshmallow import ValidationError
# from werkzeug.middleware.proxy_fix import ProxyFix
#
# # from app import connex_app, app
# from config import sa, ma, app
# from models.repositories import ItemRepo
# from flask_restx import Api, Resource, fields
# from flask import request
#
# from models.schemas import ItemSchema
#
# app.wsgi_app = ProxyFix(app.wsgi_app)
# api = Api(app)
#
# ns1 = api.namespace('item', description='item operations')
#
# item_request = api.model('Item', {
#     'id': fields.String(required=False, description='Item ID'),
#     'name': fields.String(required=True, description='Full name in English'),
#     'price': fields.String(required=True, description='Full price '),
# })
#
# item_url = api.model('ItemURL', {
#     'url': fields.String(required=True, description='URL for that item'),
# })
#
#
# ITEM_NOT_FOUND = "Item not found for id: {}"
# GEN_ERROR = "Error  occures: {}"
#
# itemRepo = ItemRepo()
# itemSchema = ItemSchema()
# itemListSchema = ItemSchema(many=True)
#
#
#
# @ns1.route('/')
# @ns1.response(400, 'Object failed scheme validation')
# @ns1.response(409, 'Person already exist')
# class ItemList(Resource):
#
#     @ns1.doc('list_item')
#     @ns1.marshal_with(item_request, skip_none=True)
#     def getAll(self):
#         return itemListSchema.dump(itemRepo.fetchAll()), 200
#
#
#
#     @ns1.doc('create_item')
#     @ns1.expect(item_request)
#     @ns1.marshal_list_with(item_request,  skip_none=True)
#     def post(self):
#         item_req_json = request.get_json()
#         item_data = itemSchema.load(item_req_json)
#         itemRepo.create(item_data)
#         return itemSchema.dump(item_data),201
#
#
# @ns1.route('/<string:id>')
# @ns1.response(404, 'Item not found')
# @ns1.param('id', 'Item ID')
# class Todo(Resource):
#     @ns1.doc('get_item')
#     @ns1.marshal_with(item_request, skip_none=True)
#     def get(self,id):
#         item_data = itemRepo.fetchById(id)
#         if item_data:
#             return itemSchema.dump(item_data)
#         return {'message': ITEM_NOT_FOUND.format(id)}, 404
#
#
#     @ns1.doc('delete_item')
#     @ns1.response(204, 'Item deleted')
#     def delete(self,id):
#         item_data = itemRepo.fetchById(id)
#         if item_data:
#             itemRepo.delete(id)
#             return {'message': 'Item deleted successfully'}, 200
#         return {'message': ITEM_NOT_FOUND.format(id)}, 404
#
#
#     @ns1.expect(item_request)
#     @ns1.marshal_with(item_request, skip_none=True)
#     @ns1.response(400, 'Object failed scheme validation')
#     @ns1.response(409, 'item already exist')
#     def put(self, id):
#         item_data = itemRepo.fetchById(id)
#         item_req_json = request.get_json()
#         if item_data:
#             item_data.name = item_req_json['name']
#             item_data.price = item_req_json['price']
#             itemRepo.update(item_data)
#             return itemSchema.dump(item_data)
#         return {'message': ITEM_NOT_FOUND.format(id)}, 404
#
#
#
#     # @ns.expect(person)
#     # @ns.marshal_with(person, skip_none=True)
#     # @ns.response(400, 'Object failed scheme validation')
#     # @ns.response(409, 'Person already exist')
#     # def patch(self, person_id):
#     #     return DAO.patch(person_id, api.payload)
#
#
#
#
#
# todo = api.model('Todo', {
#     'id': fields.Integer(readonly=True, description='The task unique identifier'),
#     'task': fields.String(required=True, description='The task details')
# })
#
#
