from flask import Blueprint, jsonify, request

from .models import Post

api = Blueprint('api1',__name__, subdomain='api',)

@api.route('/forum/posts', methods=['GET'])
def posts():
    post_id = request.args.get('id')
    user_id = request.args.get('user_id')
    limit = request.args.get('limit')

    query =  Post.query

    # TODO: check if `post_id` is in fact integer
    if post_id is not None:
        query = query.filter_by(id=int(post_id))

    # TODO: check if `user_id` is in fact integer
    if user_id is not None:
        query = query.filter_by(user_id=int(user_id))

    # TODO: check if `limit` is in fact integer
    query = query.limit(10 if limit is None else int(limit))

    return jsonify([
        {
            'id': post.id,
            'data': post.data,
            'date': post.date,
            'user_id': post.user_id
        }
        for post in query.all()
    ])

