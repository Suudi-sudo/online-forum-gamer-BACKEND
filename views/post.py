from flask import request, jsonify
from models import db, Post, Like
from . import post_bp

# Route for getting all posts
@post_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{
        'post_id': post.post_id,
        'title': post.title,
        'content': post.content,
        'image_url': post.image_url,  
        'user_id': post.user_id
    } for post in posts])

# Route for creating a post (with image URL)
@post_bp.route('/', methods=['POST'])
def create_post():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    user_id = data.get('user_id')
    image_url = data.get('image_url')  

    post = Post(user_id=user_id, title=title, content=content, image_url=image_url)

    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

# Route for updating a post (with optional image URL)
@post_bp.route('/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    data = request.json
    title = data.get('title')
    content = data.get('content')
    image_url = data.get('image_url') 
    post.title = title
    post.content = content
    post.image_url = image_url  

    db.session.commit()
    return jsonify({'message': 'Post updated successfully'}), 200

# Route for deleting a post
@post_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'}), 200

# Route for searching posts
@post_bp.route('/search', methods=['GET'])
def search_posts():
    keyword = request.args.get('keyword', '')
    posts = Post.query.filter(Post.title.ilike(f'%{keyword}%') | Post.content.ilike(f'%{keyword}%')).all()
    return jsonify([{
        'post_id': post.post_id,
        'title': post.title,
        'content': post.content,
        'image_url': post.image_url,  
        'user_id': post.user_id
    } for post in posts])

# Route for liking a post
@post_bp.route('/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.json
    like = Like(user_id=data['user_id'], post_id=post_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Post liked successfully'}), 201
