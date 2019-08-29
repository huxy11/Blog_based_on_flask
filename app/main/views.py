from datetime import datetime
from flask import render_template, session, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import User, Post, Permissions

@main.route('/',  methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.is_authenticated and current_user.can(Permissions.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html',form=form, posts=posts, pagination=pagination, Permissions=Permissions)

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if not user:
        flash('No correspondent user.')
        return redirect('.index')
    return render_template('user.html', user=user)
