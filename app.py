# -*- coding: utf-8 -*-
import os, uuid, click, sys


from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from forms import RegisterForm, LoginForm, ForgotForm, ResetForm, LostForm
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 2024


# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# flask config
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db')) + '?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# flask command config
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


# database
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    emailAddress = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(20))
    lostThings = db.relationship('LostThing')
    pickThings = db.relationship('PickThing')

    def __repr__(self):
        return '<Student %r>' % self.id


class LostThing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    lostDate = db.Column(db.Date)
    contactPerson = db.Column(db.String(20))
    contactEmail = db.Column(db.String(40))
    location = db.Column(db.Integer)
    complement = db.Column(db.String(100))
    lostStudent_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<LostThing %r>' % self.id


class PickThing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    pickDate = db.Column(db.Date)
    contactPerson = db.Column(db.String(20))
    contactEmail = db.Column(db.String(40))
    location = db.Column(db.Integer)
    complement = db.Column(db.String(100))
    pickStudent_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    def __repr__(self):
        return '<PickThing %r>' % self.id


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ 注册函数 """
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        if (not Student.query.filter_by(emailAddress=registerForm.email.data).first()):
            student = Student(name=registerForm.name.data, emailAddress=registerForm.email.data,
                              password=registerForm.password.data)
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=registerForm, emailRepeatError=True)
    return render_template('register.html', form=registerForm, emailRepeatError=False)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ 登录函数 """
    loginForm = LoginForm()
    # if 'logged_in' in session:
    #     return redirect(url_for('index'))
    if request.method == 'GET' and 'login_user' in session and Student.query.filter_by(id=session['login_user']):
        loginForm.email.data = Student.query.filter_by(id=session['login_user']).first().emailAddress
        if 'remember' in session:
            loginForm.password.data = Student.query.filter_by(id=session['login_user']).first().password
            loginForm.remember.data = True
    if loginForm.validate_on_submit():
        student = Student.query.filter_by(emailAddress=loginForm.email.data).first()
        if (student and student.password == loginForm.password.data):
            session['logged_in'] = True
            session['login_user'] = student.id
            if (loginForm.remember.data):
                session['remember'] = True
            else:
                checkRememberAndPop()
            flash('Successfully logged in')
            return redirect(url_for('index'))
        elif (not student):
            checkRememberAndPop()
            app.logger.info('noEmail')
            return render_template('login.html', form=loginForm, noEmail=True)
        else:
            checkRememberAndPop()
            return render_template('login.html', form=loginForm, incorrectPassword=True)
    return render_template('login.html', form=loginForm)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    """ 忘记密码 """
    forgotForm = ForgotForm()
    if forgotForm.validate_on_submit():
        student = Student.query.filter_by(emailAddress=forgotForm.email.data).first()
        if (student):
            return redirect(url_for('reset', user_id=student.id))
        else:
            return render_template('forgot.html', form=forgotForm, noStudent=True)
    return render_template('forgot.html', form=forgotForm)


@app.route('/reset/?<int:user_id>', methods=['GET', 'POST'])
def reset(user_id):
    """ 密码重置 """
    resetForm = ResetForm()
    if resetForm.validate_on_submit():
        student = Student.query.get(user_id)
        student.password = resetForm.newPassword.data
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset.html', form=resetForm)


@app.route('/Terms and Conditions')
def Terms_and_Conditions():
    return '<h1>!!!Surprise!!!</h1>'


@app.route('/lost', methods=['GET', 'POST'])
def lost():
    lostForm = LostForm()
    if lostForm.validate_on_submit():
        return redirect(url_for('login'))
    return render_template('lost.html', form=lostForm)


@app.route('/found')
def found():
    return render_template('found.html')

def checkRememberAndPop():
    if 'remember' in session:
        session.pop('remember')