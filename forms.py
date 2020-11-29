# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError, Email

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message=u'Name is required')], render_kw={'class': 'form-control'})
    email = StringField('E-Mail Address', validators=[DataRequired(message=u'E-Mail Address is required')], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired(message=u'Password is required')], render_kw={'class': 'form-control'})
    agree = BooleanField('I agree to the <a href="#">Terms and Conditions</a>')
