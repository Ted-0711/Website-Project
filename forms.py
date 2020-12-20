# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, \
    TextAreaField, SubmitField, MultipleFileField, SelectField, DateTimeField
from wtforms.widgets.core import PasswordInput
from wtforms.validators import DataRequired, Length, ValidationError, Email, AnyOf


class MyPasswordField(PasswordField):
    widget = PasswordInput(hide_value=False)


class RegisterForm(FlaskForm):
    name = StringField(
        'Name',
       validators=[DataRequired(message=u'Name is required')],
       render_kw={'class': 'form-control'}
       )
    email = StringField(
        'E-Mail Address',
        validators=[DataRequired(message=u'Email is required'),
                    Email(message=u'Legal E-Mail Address is required')],
        render_kw={'class': 'form-control'}
        )
    password = PasswordField(
        'Password',
         validators=[DataRequired(message=u'Password is required'),
                     Length(min=8, max=20, message=u'Password must be longer than 8 digits and less than 20 digits')],
         render_kw={'class': 'form-control'}
         )
    agree = BooleanField(
        'Agree',
         validators=[AnyOf([True], message=u'You must agree with our Terms and Conditions')],
         render_kw={'class': 'custom-control-input', 'required': ''}
         )


class LoginForm(FlaskForm):
    email = StringField(
        'E-Mail Address',
        validators=[DataRequired(message=u'Email is required'),
                    Email(message=u'Legal E-Mail Address is required')],
        render_kw={'class': 'form-control'}
        )
    password = MyPasswordField(
        'Password',
       validators=[DataRequired(message=u'Password is required')],
       render_kw={'class': 'form-control'}
       )
    remember = BooleanField(
        'Remember Me',
        render_kw={'class': 'custom-control-input'}
        )


class ForgotForm(FlaskForm):
    email = StringField(
        'E-Mail Address',
        validators=[DataRequired(message=u'Email is required'),
                    Email(message=u'Legal E-Mail Address is required')],
        render_kw={'class': 'form-control'}
        )


class ResetForm(FlaskForm):
    newPassword = PasswordField(
        'New Password',
        validators=[DataRequired(message=u'Password is required'),
                    Length(min=8, max=20, message=u'Password must be longer than 8 digits and less than 20 digits')],
        render_kw={'class': 'form-control'}
        )


class LostForm(FlaskForm):
    itemType = SelectField(
        'Item Type',
        validators=[DataRequired(message=u'ItemType is required')],
        choices=[('1', 'License'), ('2', 'Digital device'), ('3', 'Jewelry and Ornament'), ('4', 'Cosmetics and Daily supplies'), ('5', 'Clothes and Shoes'), ('6', 'Books and Files')],
        render_kw={'class': 'form-control'}
        )
    itemName = StringField(
        'Item Name',
        validators=[DataRequired(message=u'Item name is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please enter the item name'}
       )
    contactPerson = StringField(
        'Contact Person',
        validators=[DataRequired(message=u'Contact person is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please enter the contact person'}
       )
    emailAddress = StringField(
        'E-Mail Address',
        validators=[DataRequired(message=u'E-Mail address is required'), Email(message=u'Legal E-Mail Address is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please enter the e-mail address'}
        )
    lostLocation = StringField(
        'place',
        validators=[DataRequired(message=u'Lost location is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please click the lost location in the map', 'readonly': 'readonly'}
    )
    complement = TextAreaField(
        'Complement (optional)',
        render_kw={'class': 'form-control', 'rows': '5', 'placeholder': 'Please enter additional information here'}
    )


class FoundForm(FlaskForm):
    itemType = SelectField(
        'Item Type',
        validators=[DataRequired(message=u'ItemType is required')],
        choices=[('1', 'License'), ('2', 'Digital device'), ('3', 'Jewelry and Ornament'), ('4', 'Cosmetics and Daily supplies'), ('5', 'Clothes and Shoes'), ('6', 'Books and Files')],
        render_kw={'class': 'form-control'}
        )
    itemName = StringField(
        'Item Name',
        validators=[DataRequired(message=u'Item name is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please enter the item name'}
       )
    contactPerson = StringField(
        'Contact Person',
        validators=[DataRequired(message=u'Contact person is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please enter the contact person'}
       )
    emailAddress = StringField(
        'E-Mail Address',
        validators=[DataRequired(message=u'E-Mail address is required'), Email(message=u'Legal E-Mail Address is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please enter the e-mail address'}
        )
    foundLocation = StringField(
        'place',
        validators=[DataRequired(message=u'Found location is required')],
        render_kw={'class': 'form-control', 'placeholder': 'Please click the found location in the map', 'readonly': 'readonly'}
    )
    complement = TextAreaField(
        'Complement (optional)',
        render_kw={'class': 'form-control', 'rows': '5', 'placeholder': 'Please enter additional information here'}
    )