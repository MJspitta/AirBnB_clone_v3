#!/usr/bin/python3
"""create new view for state obj"""

from flask import abort, jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """get list of all state obj"""
    states = storage.all(State).values()
    state_lst = [state.to_dict() for state in states]
    return jsonify(state_lst)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get state obj"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes state obj"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates state obj"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updates state obj"""
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for k, v in data.items():
            if k not in ignore_keys:
                setattr(state, k, v)
        state.save()
        return jsonify(state.to_dict()), 200
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
