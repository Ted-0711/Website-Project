# -*- coding: utf-8 -*-
import os
import uuid

from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from forms import RegisterForm
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('register'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    app.logger.info('\nname: %s\nemail: %s\npassword: %s', registerForm.name.data, registerForm.email.data,
                    registerForm.password.data)
    app.logger.info(registerForm.errors)
    for content in registerForm:
        app.logger.info(content.label)
    if registerForm.validate_on_submit():
        return redirect(url_for('forgot'))
    return render_template('register.html', form=registerForm)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    return


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    return render_template('forgot.html')
