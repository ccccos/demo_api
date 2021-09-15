from flask import Flask, jsonify, make_response, request
import json
import os
import sys
sys.path.insert(0, os.getcwd())
from app.post import PostCollection

def create_app():

    app = Flask(__name__)

    @app.route('/api/ping')
    def ping():
        respond = jsonify({'success':True})
        return make_response(respond, 200)


    @app.route('/api/posts', methods=['GET'])
    def get_posts():
        tags = request.args.get('tags')
        if not tags:
            respond = jsonify({'error':'Tags parameter is required'})
            return make_response(respond, 400)
        tag_list = tags.split(',')

        valid_sort_value = ['id', 'reads', 'likes', 'popularity']
        sortBy = request.args.get('sortBy')
        direction = request.args.get('direction')
        if sortBy:
            if sortBy not in valid_sort_value:
                respond = jsonify({'error':'sortBy parameter is invalid'})
                return make_response(respond, 400)
        else:
            sortBy = 'id'
        if direction:
            if direction not in ['asc', 'desc']:
                respond = jsonify({'error':'sortBy parameter is invalid'})
                return make_response(respond, 400)
        else:
            direction = 'asc'
        #TODO: query the api and return result.
        post_collection = PostCollection()
        post_collection.get_posts(tags=tag_list)
        post_collection.sort(sortBy, direction)
        return make_response(jsonify(post_collection.posts), 200)
    return app