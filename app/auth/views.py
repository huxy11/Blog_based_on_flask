from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from .. import db
from ..models import User
from ..decorators import admin_required, permission_required
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, EditProfileForm, AdminIdQueryForm, UserProfileForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()

@auth.route('/admin')
@login_required
@admin_required
def admin_only():
    return "Welcom administrator!"


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.account.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid account or password.')
    return render_template('auth/login.html', form=form)
    #the template file is located at app/templates/auth

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.account.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration completed.')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/<username>')
@login_required
def account(username):
    if not current_user.is_authenticated or not current_user.username == username:
        abort(404)
    else:
        return render_template('auth/account.html')

@auth.route('/<username>/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile(username):
    if not current_user.is_authenticated or current_user.username != username:
        abort(404)
    else:
        form = EditProfileForm()
        if form.validate_on_submit():
            current_user.location = form.location.data
            current_user.about_me = form.about_me.data
            db.session.add(current_user)
            db.session.commit()
            flash('Info has been changed.')
            return redirect(url_for('.account', username=current_user.username)) 
        else:
            form.location.data = current_user.location
            form.about_me.data = current_user.about_me
            return render_template('auth/edit_profile.html', form=form)

@auth.route('/<username>/chgpsw', methods=['GET','POST'])
@login_required
def change_password(username):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
                current_user.password = form.password.data
                db.session.add(current_user)
                db.session.commit()
                flash('Password has been changed.')
                logout_user()
                return redirect(url_for('.login'))
        else:
            flash('Invalid old password')
    return render_template('auth/change_password.html', form=form)

@auth.route('/admin/', methods=['GET', 'POST'])
@login_required
@admin_required
def admin():
    form = AdminIdQueryForm()
    if form.validate_on_submit():
        usr = User.query.filter_by(id=form.id.data).first()
        if not usr:
            flash('No Correspondent User.')
            session['id'] = None
        else:
            session['id'] = usr.id
        return redirect(url_for('.admin'))
    usr = User.query.filter_by(id=session.get('id')).first()
    return render_template('auth/admin.html', form=form, usr=usr)


@auth.route('/admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user_profile(id):
    form = UserProfileForm()
    user = User.query.filter_by(id=id).first()
    if not user:
        flash('No correspondent user.')
        return redirect(url_for('.admin'))
    if form.validate_on_submit():
        user.username = form.username.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('User\'s profile has been changed.')
        return redirect(url_for('.edit_user_profile', id=id))
    form.username.data = user.username
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('auth/edit_user_profile.html', form=form) 
