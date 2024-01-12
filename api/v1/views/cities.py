#!/usr/bin/python3
"""
This is a script file contains the City module
"""
from flask import make_response, request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flasgger.utils import swag_from


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/city/get.yml', methods=['GET'])
def get_cities(state_id):
    """ This is a methods that gets cities for state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/city/get_id.yml', methods=['GET'])
def get_city(city_id):
    """ This is a mothod that get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/city/delete.yml', methods=['DELETE'])
def del_city(city_id):
    """ This is a method that delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/city/post.yml', methods=['POST'])
def create_obj_city(state_id):
    """ This is a method that post/create new instance """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)

    js = request.get_json()
    obj = City(**js)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/city/put.yml', methods=['PUT'])
def post_city(city_id):
    """ This is amethod the return the new cities Id """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
