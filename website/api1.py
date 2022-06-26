from flask import Blueprint, jsonify, request
from requests import post, session

from .models import Post

api = Blueprint('api1',__name__, subdomain='api',)

@api.route('/forum/posts', methods=['GET'])
def posts():
    query_parameters = request.args
    
    id = query_parameters.get('id')
    user_id = query_parameters.get('user_id')
    limit = query_parameters.get('limit')

    query =  Post.query
 
    if id: 
        query = query.filter_by(id=id)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if limit:
        query = query.limit(limit)
    if not limit:
        query = query.limit(10)

    posts = []
    for post in query.all():
        posts.append(
            {
                'id': post.id, 'data': post.data, 'date': post.date, 'user_id': post.user_id
            }
        )
    return jsonify(posts)

