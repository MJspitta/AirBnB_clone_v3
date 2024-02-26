#!/usr/bin/python3
"""create new view for user obj"""

from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """get list of all user obj"""
    users = storage.all(User).values()
    user_lst = [user.to_dict() for user in users]
    return jsonify(user_lst)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get user obj"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes user obj"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """creates user obj"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'email' not in kwargs:
        abort(400, 'Missing email')
    if 'password' not in kwargs:
        abort(400, 'Missing password')
    user = User(**kwargs)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """updates user obj"""
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in ignore_keys:
                setattr(user, k, v)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.errorhandler(404)
def not_found(error):
    """raise 404 error"""
    resp = {'error': 'Not found'}
    return jsonify(resp), 404


@app_views.errorhandler(400)
def bad_request(error):
    """returns bad request message for illegal requests"""
    resp = {'error': 'Bad Request'}
    return jsonify(resp), 400
