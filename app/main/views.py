from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import login_required, current_user
from . import main
from .forms import PostForm
from .. import db
from ..models import User, Post, Permissions

@main.route('/')
def index():
    form = PostForm()
    if current_user.is_authenticated and current_user.can(Permissions.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html',form=form, posts=posts, Permissions=Permissions)
