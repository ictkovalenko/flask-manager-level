from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from datetime import datetime
from app import db, app_version

performers = Blueprint('performers', __name__)


@performers.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        dt = datetime.now()
        current_user.last_login_date = dt
        db.session.commit()
        context = dict()
        context['app_version'] = app_version
        return render_template('performers/index.html', context=context)
    else:
        return redirect(url_for('accounts.login'))
