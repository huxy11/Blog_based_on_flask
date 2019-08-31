from flask import current_app
from datetime import datetime
from . import db
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from markdown import markdown
import bleach

class Permissions:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTRATOR = 0x80

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
                'User' : (Permissions.FOLLOW | Permissions.COMMENT | Permissions.WRITE_ARTICLES, True),
                'Moderator' : (Permissions.FOLLOW | Permissions.COMMENT | Permissions.WRITE_ARTICLES | Permissions.MODERATE_COMMENTS, False),
                'Admin':(0xff, False)
                }
        for r in roles:
            role =Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        admin = User.query.filter_by(username=current_app.config['ADMIN_NAME']).first()
        if admin is None:
            admin = User(username= current_app.config['ADMIN_NAME'], password=current_app.config['ADMIN_PASSWORD'])
            db.session.add(admin)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    #Setting Permissions
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.role is None:
                if self.username == current_app.config['ADMIN_NAME']:
                    self.role = Role.query.filter_by(permissions=0xff).first()
                else:
                    self.role = Role.query.filter_by(default=True).first()

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')
    follower = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')
    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permissions.ADMINISTRATOR)

    #password is read-only
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None
    
    def is_followed_by(self, user):
        return self.follower.filter_by(follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self,followed=user)
            db.session.add(follow)
            db.session.commit()
    def unfollow(self, user):
        follow = self.followed.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)

    def __repr__(self):
        return '<User %r>' % self.username


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    #target_id = db.Column(db.Intger)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr','acronym', 'b', 'blockquote', 'code', 'em', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)



class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False
