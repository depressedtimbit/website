from flask import Blueprint, jsonify, redirect, request, abort, url_for
from flask_cors import cross_origin
from flask_login import current_user, login_required
from website import db
from .models import Post, User

api = Blueprint('api1',__name__, subdomain='api',)



@api.route('/forum/posts', methods=['GET'])
@cross_origin("http://api.checkhost.local:5000/") 
def posts():
    page = request.args.get('page')
    index = request.args.get('index')
    post_id = request.args.get('id')
    user_id = request.args.get('user_id')
    
    query =  Post.query

    query = query.order_by(Post.id.desc())

    # TODO: check if `post_id` is in fact integer
    if post_id is not None:
        query = query.filter_by(id=int(post_id))

    # TODO: check if `user_id` is in fact integer
    if user_id is not None:
        query = query.filter_by(user_id=int(user_id))

    # TODO: check if `limit` is in fact integer
    if index is None:
        index = 10
    query = query.limit(int(index))

    if page is None:
        abort(400)
    query = query.offset(int(page) * int(index))

    if not query.all():
        abort(404)

    return jsonify([
        {
            'id': post.id,
            'data': post.data,
            'date': post.date.timestamp(),
            'user_id': post.user_id,
            'username': User.query.get(int(post.user_id)).username
        }
        for post in query.all()
    ])

@api.route('/forum/delete-post', methods=['POST'])
@login_required
def delete_post():
    post_id = request.form.get('postid')
    if post_id is None:
        abort(400)
    post = Post.query.get(int(post_id))
    if post is None:
        abort(410)
    if post.user_id is not current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('views.Forum'))