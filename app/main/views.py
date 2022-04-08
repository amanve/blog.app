from flask import (url_for, request, render_template)
from . import main
from .. import db
from ..models import Post
from sqlalchemy import desc


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.dateCreated)).paginate(
        page, main.config['POSTS_PER_PAGE'], True)
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html',
                           posts=posts,
                           next_url=next_url,
                           prev_url=prev_url)
