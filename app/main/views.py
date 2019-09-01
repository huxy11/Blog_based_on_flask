from datetime import datetime
from flask import render_template, session, redirect, url_for, request, current_app, flash

from flask_login import login_required, current_user
from . import main
from .forms import CommentForm
from .. import db
from ..models import User, Comment, Permissions, Post
from ..decorators import admin_required
from ..auth.forms import PostForm

@main.route('/',  methods=['GET', 'POST'])
def index():
    form = CommentForm()
    if current_user.is_authenticated and current_user.can(Permissions.WRITE_ARTICLES) and form.validate_on_submit():
        comment = Comment(body=form.body.data, author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=current_app.config['COMMENTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('index.html',form=form, comments=comments, pagination=pagination, Permissions=Permissions)
@main.route('/posts')
def posts():
    page = request.args.get('pqge', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('posts.html',posts=posts,pagination=pagination)
@main.route('/posts/<int:id>')
def post_id(id):
    post = Post.query.get_or_404(id)
    return render_template('post_id.html', post=post)
@main.route('/posts/<int:id>/edit', methods=['GET','POST'])
@login_required
@admin_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('Post has been changed.')
        return redirect(url_for(post_id, id=id))
    form.title.data = post.title
    form.body.data = post.body
    return render_template("edit_post.html", form=form)

@main.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        flash('The user you want to follow does not exist.')
        return redirect(url_for('.index'))

    current_user.follow(user)
    if current_user.is_following(user):
        flash('Successfully followed.')
    return redirect(url_for('main.user', username=user.username))


@main.route('/unfollow/<int:user_id>')
@login_required
def unfollow(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('The user yout want to unfollow does not exist.')
        return redirec(url_for('.index'))
    if current_user.is_following(user):
        current_user.unfollow(user)
        if not current_user.is_following(user):
            flash('Successfully unfollowed.')
    return redirect(url_for('.user', username=user.username))
    

@main.route('/user/<username>/followers')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.follower.paginate(page, per_page=current_app.config['FOLLOWS_PER_PAGE'],error_out=False)
    follows = [{'user':item.follower, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('follows.html', user=user, title="Followers of", endpoint='.followers', pagination=pagination, follows = follows)
@main.route('/user/<username>/following')
def following(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Invalid user')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(page, per_page=current_app.config['FOLLOWS_PER_PAGE'],error_out=False)
    follows = [{'user':item.followed, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('follows.html', user=user, title="Followed by", endpoint='.following', pagination=pagination, follows = follows)

@main.route('/user/<username>')
def user(username):
    user=User.query.filter_by(username=username).first()
    if not user:
        flash('No correspondent user.')
        return redirect('.index')
    comments = user.comments.order_by(Comment.timestamp.desc()).all()
    return render_template('user.html', user=user, Permissions=Permissions, comments=comments)
