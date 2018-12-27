from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app_version, db
from app.models import User
from .forms import LoginForm, PasswordForm, AdminProfileForm
from . import admin_required

accounts = Blueprint('accounts', __name__)


@accounts.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    page = request.args.get('page', 1, type=int)
    pagination = User.query.filter(User.login != 'admin').paginate(
        page, per_page=current_app.config['ITEMS_PER_PAGE'],
        error_out=False)
    context = dict()
    context['users'] = pagination.items
    context['pagination'] = pagination
    context['app_version'] = app_version
    return render_template('accounts/index.html', context=context)


@accounts.route('/login', methods=['GET', 'POST'])
# def login():
#     # only for debug
#     user = User.query.filter_by(login='admin').first()
#     if user is not None:
#         login_user(user, True)
#         return redirect(url_for('performers.index'))
#     else:
#         abort(500)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None:
            # first time login
            if user.has_password:
                if user.verify_password(form.password.data):
                    login_user(user, form.remember_me.data)
                    # next_var = request.args.get('next')
                    # if next_var is None or not next_var.startswith('/'):
                    #     next_var = url_for('performers.index')
                    return redirect(url_for('performers.index'))
                else:
                    flash(u'wrong pass')
            else:
                return redirect(url_for('.setpassword', user_id=user.id))
        else:
            flash(u'user not found')
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/login.html', context=context)


@accounts.route('/logout')
@login_required
def logout():
    flash(u'logged out')
    logout_user()
    return redirect(url_for('performers.index'))


@accounts.route('/setpassword/<int:user_id>', methods=['GET', 'POST'])
def setpassword(user_id):
    form = PasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            if user.has_password:
                flash(u'already set')
            else:
                user.password = form.password.data
                user.has_password = True
                db.session.add(user)
                db.session.commit()
                flash(u'Pass saved')
        else:
            flash(u'user not found')
        return redirect(url_for('.index'))
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/setpassword.html', context=context)


@accounts.route('/resetpassword', methods=['POST'])
@login_required
def resetpassword():
    user = User.query.filter_by(login=request.form['login']).first()
    user.has_password = False
    db.session.add(user)
    db.session.commit()
    flash(u'Pass flushed')
    return redirect(url_for('.edituser', user_id=user.id))


@accounts.route('/newuser', methods=['GET', 'POST'])
@login_required
@admin_required
def newuser():
    form = AdminProfileForm(edit=False)
    if form.validate_on_submit():
        user = User()
        user.login = form.login.data
        user.name_first = form.name_first.data
        user.name_last = form.name_last.data
        user.name_middle = form.name_middle.data
        user.email = form.email.data
        user.role = form.role.data
        user.company = form.company.data
        user.city = form.city.data
        user.contacts = form.contacts.data
        db.session.add(user)
        db.session.commit()
        flash(u'User created')
        return redirect(url_for('.index'))
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/profile.html', context=context)


@accounts.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edituser(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404)

    form = AdminProfileForm(obj=user, edit=True)
    if form.validate_on_submit():
        user.name_first = form.name_first.data
        user.name_last = form.name_last.data
        user.name_middle = form.name_middle.data
        user.email = form.email.data
        user.role = form.role.data
        user.company = form.company.data
        user.city = form.city.data
        user.contacts = form.contacts.data
        db.session.add(user)
        db.session.commit()
        flash(u'User updated')
        return redirect(url_for('.index'))
    context = dict()
    context['form'] = form
    context['app_version'] = app_version
    return render_template('accounts/profile.html', context=context)


@accounts.route('/deleteuser', methods=['POST'])
@login_required
@admin_required
def deleteuser():
    User.query.filter_by(login=request.form['login']).delete()
    db.session.commit()
    flash(u'User deleted')
    return redirect(url_for('.index'))
