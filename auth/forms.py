from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur","autofocus":""})
    password = PasswordField(validators=[DataRequired()],  render_kw={"placeholder": "Mot de passe"})
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={"placeholder": "Nom d'utilisateur","autofocus":""})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "E-mail"})
    password = PasswordField(validators=[DataRequired()],  render_kw={"placeholder": "Mot de passe"})
    password2 = PasswordField(validators=[DataRequired(),EqualTo('password')],  render_kw={"placeholder": "Répéter le mot de passe"})
    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')