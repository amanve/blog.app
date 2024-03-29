from datetime import datetime

import pandas as pd
from app.main.forms import ContactUs, NewComment, NewPost
from flask import current_app, redirect, render_template, request, url_for, flash, abort
from flask_security import current_user, login_required
from sqlalchemy import desc

from .. import db
from ..models import Comments, Post
from . import main


#Custom Templates
@main.app_template_filter('datetime_format')
def datetime_format(value, format='%d %B,%Y'):
    if value == None:
        return None
    return value.strftime(format)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(desc(Post.dateCreated)).paginate(
        page, current_app.config['POSTS_PER_PAGE'], True)
    next_url = url_for('.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('.index', page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('index.html',
                           posts=posts,
                           next_url=next_url,
                           prev_url=prev_url)


@main.route('/post/<post_id>/<slug_url>', methods=['GET', 'POST'])
def post(post_id, slug_url):
    form = NewComment()
    post = Post.query.get(int(post_id))
    comments_page = request.args.get('comments_page', 1, type=int)

    if form.validate_on_submit():
        comment = Comments(name=form.name.data,
                           email=form.email.data,
                           comment=form.comment.data,
                           dateCreated=datetime.now())
        post.comments.append(comment)
        db.session.commit()

        return redirect(url_for('.post', post_id=post.id, slug_url=slug_url))

    comments = Comments.query.filter_by(post_id=post_id).order_by(
        desc(Comments.dateCreated)).paginate(
            comments_page, current_app.config['COMMENTS_PER_PAGE'], True)
    # comments = Comments.query.filter_by(post_id=post_id).all()
    next_url = url_for('.post', comments_page=comments.next_num, post_id=post.id) \
    if comments.has_next else None
    prev_url = url_for('.post', comments_page=comments.prev_num, post_id=post.id) \
    if comments.has_prev else None

    return render_template('post.html',
                           post=post,
                           form=form,
                           comments=comments,
                           next_url=next_url,
                           prev_url=prev_url,
                           title=post.heading)


@main.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    form = NewPost()
    if form.validate_on_submit():
        new_post = Post(heading=form.heading.data,
                        subHeading=form.subHeading.data,
                        body=form.body.data,
                        dateCreated=datetime.now(),
                        user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('.index'))

    return render_template('add_post.html', form=form)


@main.route('/about')
def about():
    return render_template('about.html')


# @main.route('/contact', methods=['GET', 'POST'])
# def contact():
#     form = ContactUs()

#     if form.validate_on_submit():
#         name = request.form['name']
#         email = request.form['email']
#         telephone = request.form['telephone']
#         message = request.form['message']
#         res = pd.DataFrame({
#             'name': [name],
#             'email': [email],
#             'telephone': [telephone],
#             'message': [message],
#             'datetime': [datetime.strftime(datetime.now(), '''%d/%m/%y''')]
#         })
#         res.to_csv(current_app.config['CONTACT_MSG_PATH'],
#                    mode='a',
#                    index=False)
#         # Todo
#         """ Delete data as per datetime - need to figure out """

#         return redirect(url_for('main.contact'))

#     return render_template('contact.html', form=form)


@main.route('/edit/<post_id>/<slug_url>', methods=['GET', 'POST'])
@login_required
def edit(post_id, slug_url):
    post = Post.query.get_or_404(post_id)
    form = NewPost()
    if request.method == 'POST':
        body = request.form['body']
        post.body = body

        db.session.add(post)
        db.session.commit()
        flash("Post has been updated!")

        return redirect(
            url_for('.post', post_id=post.id, slug_url=post.slug_url))

    form.body.data = post.body
    return render_template('edit_post.html', form=form, post=post)
