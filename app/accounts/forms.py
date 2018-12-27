from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp
from app.models import Roles, User
from wtforms import ValidationError


class LoginForm(FlaskForm):
    login = StringField(u'Login', validators=[
        DataRequired(u'R-field'),
        Length(1, 128)])
    password = PasswordField(u'Pass', validators=[DataRequired(u'R-field')])
    remember_me = BooleanField(u'rememberme')
    submit = SubmitField(u'Auth')


class PasswordForm(FlaskForm):
    password = PasswordField(u'Pass', validators=[
        DataRequired(u'R-field'),
        Length(min=6, max=128, message=u'not less then 6 chars'),
        EqualTo('confirm', message=u'not identical')])
    confirm = PasswordField(u're-enter')
    submit = SubmitField(u'Save')


class AdminProfileForm(FlaskForm):
    name_last = StringField(u'first', validators=[DataRequired(u'R-field'), Length(1, 128)])
    name_first = StringField(u'last', validators=[DataRequired(u'R-field'), Length(1, 128)])
    name_middle = StringField(u'middle')
    email = StringField(u'e-mail', validators=[DataRequired(u'R-field'), Length(1, 128), Email()])
    company = StringField(u'Org', validators=[Length(max=255)])
    city = StringField(u'Location', validators=[Length(max=255)])
    contacts = StringField(u'Phone', validators=[Length(max=255)])
    login = StringField(u'Login', validators=[
        DataRequired(u'R-field'),
        Length(1, 128),
        Regexp('^[A-Za-z0-9_]+$',
               message=u'only digits, alphabet and - . _')])
    role = SelectField(u'role', coerce=int)

    def __init__(self, edit, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        self.role.choices = [
            (Roles.USER, Roles.USER_NAME),
            (Roles.MANAGER, Roles.MANAGER_NAME),
            (Roles.ADMIN, Roles.ADMIN_NAME)
        ]
        self.edit = edit

    def validate_login(self, field):
        if not self.edit:
            if User.query.filter_by(login=field.data).first():
                raise ValidationError(u'already used')
