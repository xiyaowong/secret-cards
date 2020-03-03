from flask import jsonify, g, request

from back_end.models import User, Post, db
from back_end.api.auth import auth_required
from back_end.api.errors import bad_request, error_response

# TODO: 增删改查


def login():
    try:
        username = request.json["username"] or request.values["username"]
        password = request.json["password"] or request.values["password"]
    except:
        return bad_request("Please give me a valid data!")

    if not username or not password:
        return bad_request("Please give me a valid data!")
    user = User.query.filter_by(username=username).first()
    if not user:
        return error_response(404, "The username does not exist.")
    if not user.check_password(password):
        return bad_request("wrong password")
    token = user.generate_token()
    return jsonify({"token": token})


@auth_required
def get_user_info():
    """
    当前用户信息
    """
    return jsonify(g.current_user.to_dict())


@auth_required
def get_user_posts():
    """
    当前用户帖子
    """
    posts = g.current_user.posts
    data = [post.to_dict() for post in posts]
    return jsonify(data)


def get_user_post_by_id(user_id):
    """
    获取指定用户id的帖子
    """
    post = Post.query.filter_by(author_id=user_id).first()
    return jsonify(post.to_dict())


def add_user():
    """
    添加用户
    """
    try:
        username = request.json["username"] or request.values["username"]
        password = request.json["password"] or request.values["password"]
    except:
        return bad_request("Please give me a valid data!")

    if not username or not password:
        return bad_request("Please give me a valid data!")

    if User.query.filter_by(username=username).first():
        return bad_request("The username is already existed.")

    user = User()
    user.username = username
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict())


def get_posts():
    """
    return all posts, it could be extremely large!
    """
    posts = Post.query.all()
    data = [post.to_dict() for post in posts]
    return jsonify(data)


@auth_required
def add_post():
    """
    新增帖子
    """
    user = g.current_user
    try:
        content = request.json["content"] or request.values["content"]
    except:
        return bad_request("Please give me a valid data!")
    if not content:
        return bad_request("Please give me a valid data!")
    post = Post()
    post.author_id = user.id
    post.content = content
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict())


def post_detail(post_id):
    """
    帖子详情
    """
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


def init_bp(bp):
    bp.add_url_rule("/user/", "get_user_info", get_user_info)
    bp.add_url_rule("/user/", "login", login, methods=['POST'])
    bp.add_url_rule("/user/posts/", "get_user_posts", get_user_posts)
    bp.add_url_rule("/users/<user_id>/posts/",
                    "get_user_post_by_id", get_user_post_by_id)
    bp.add_url_rule("/users/", "add_user",  add_user, methods=['POST'])
    bp.add_url_rule("/posts/", "get_posts", get_posts)
    bp.add_url_rule("posts/<post_id>/", "post_detail", post_detail)
    bp.add_url_rule("/posts/", "add_post", add_post, methods=['POST'])
