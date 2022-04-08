from datetime import datetime

import pandas as pd
from flask import (redirect, render_template, request, url_for)
from flask_security import (current_user, login_required)
from flask_sqlalchemy import desc

from app import app, db
from app.forms import ContactUs, NewComment, NewPost
from app.models import Comments, Post


#Custom Templates
@app.template_filter('datetime_format')
def datetime_format(value, format='%d %B,%Y'):
    if value == None:
        return None
    return value.strftime(format)


#Register Routes


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post(post_id):
    form = NewComment()
    post = Post.query.get(int(post_id))
    comments_page = request.args.get('comments_page', 1, type=int)

    if form.validate_on_submit():
        comment = Comments(user_id=current_user.id,
                           comment=form.comment.data,
                           dateCreated=datetime.now())
        post.comments.append(comment)
        db.session.commit()

        return redirect(url_for('post', post_id=post.id))

    comments = Comments.query.filter_by(post_id=post_id).order_by(
        desc(Comments.dateCreated)).paginate(comments_page,
                                             app.config['COMMENTS_PER_PAGE'],
                                             True)
    # comments = Comments.query.filter_by(post_id=post_id).all()

    next_url = url_for('post', comments_page=comments.next_num, post_id=post.id) \
    if comments.has_next else None
    prev_url = url_for('post', comments_page=comments.prev_num, post_id=post.id) \
    if comments.has_prev else None

    return render_template('post.html',
                           post=post,
                           form=form,
                           comments=comments,
                           next_url=next_url,
                           prev_url=prev_url)


@app.route('/add_post', methods=['GET', 'POST'])
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

        return redirect(url_for('index'))

    return render_template('add_post.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactUs()

    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        telephone = request.form['telephone']
        message = request.form['message']
        res = pd.DataFrame({
            'name': [name],
            'email': [email],
            'telephone': [telephone],
            'message': [message],
            'datetime': [datetime.strftime(datetime.now(), '''%d/%m/%y''')]
        })
        res.to_csv('../contactusMessage.csv', mode='a', index=False)
        # Todo
        """ Delete data as per datetime - need to figure out """

        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)
