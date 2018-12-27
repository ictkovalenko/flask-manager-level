from flask import Blueprint, render_template
from flask_login import login_required
from app import app_version
from app.accounts import notuser_required

party = Blueprint('party', __name__)


@party.route('/', methods=['GET', 'POST'])
@login_required
@notuser_required
def index():
    context = dict()
    context['app_version'] = app_version
    return render_template('party/index.html', context=context)
