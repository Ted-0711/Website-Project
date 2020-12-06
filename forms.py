# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField
from wtforms.widgets.core import PasswordInput
from wtforms.validators import DataRequired, Length, ValidationError, Email, AnyOf


class MyPasswordField(PasswordField):
    widget = PasswordInput(hide_value=False)


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message=u'Name is required')], render_kw={'class': 'form-control'})
    email = StringField('E-Mail Address', validators=[DataRequired(message=u'Email is required'), Email(message=u'Legal E-Mail Address is required')], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired(message=u'Password is required'), Length(min=8, max=20, message=u'Password must be longer than 8 digits and less than 20 digits')], render_kw={'class': 'form-control'})
    agree = BooleanField('Agree', validators=[AnyOf([True], message=u'You must agree with our Terms and Conditions')], render_kw={'class': 'custom-control-input', 'required': ''})


class LoginForm(FlaskForm):
    email = StringField('E-Mail Address', validators=[DataRequired(message=u'Email is required'), Email(message=u'Legal E-Mail Address is required')], render_kw={'class': 'form-control'})
    password = MyPasswordField('Password', validators=[DataRequired(message=u'Password is required')], render_kw={'class': 'form-control'})
    remember = BooleanField('Remember Me', render_kw={'class': 'custom-control-input'})


class ForgotForm(FlaskForm):
    email = StringField('E-Mail Address', validators=[DataRequired(message=u'Email is required'), Email(message=u'Legal E-Mail Address is required')], render_kw={'class': 'form-control'})


class ResetForm(FlaskForm):
    newPassword = PasswordField('New Password', validators=[DataRequired(message=u'Password is required'), Length(min=8, max=20, message=u'Password must be longer than 8 digits and less than 20 digits')], render_kw={'class': 'form-control'})
