# -*- coding: utf-8 -*-
import os, uuid, click, sys, math


from flask import Flask, render_template, flash, redirect, url_for, request, send_from_directory, session
from forms import RegisterForm, LoginForm, ForgotForm, ResetForm, LostForm, FoundForm
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


def convert_coor_to_pixelcoor(coor):
    lib_coor = (121.218355, 31.292920)
    star_coor = (121.224631, 31.293527)
    lib_pixelcoor = (470, 252)
    star_pixelcoor = (218, 223)
    # app.logger.info('coor')
    # app.logger.info(coor)
    # app.logger.info('coor[0] - lib_coor[0]')
    # app.logger.info(coor[0] - lib_coor[0])
    # app.logger.info('star_coor[0] - lib_coor[0]')
    # app.logger.info(star_coor[0] - lib_coor[0])
    # app.logger.info(lib_pixelcoor[0] + (coor[0] - lib_coor[0]) / (star_coor[0] - lib_coor[0]) * (star_pixelcoor[0] - lib_pixelcoor[0]))
    return (lib_pixelcoor[0] + ((coor[0] - lib_coor[0]) / (star_coor[0] - lib_coor[0])) * ((star_pixelcoor[0] - lib_pixelcoor[0])),
            lib_pixelcoor[1] + ((coor[1] - lib_coor[1]) / (star_coor[1] - lib_coor[1])) * (star_pixelcoor[1] - lib_pixelcoor[1]))


def convert_type(num_type):
    type_dict = {1: 'License', 2: 'Digital device', 3: 'Jewelry and Ornament', 4: 'Cosmetics and Daily supplies', 5: 'Clothes and Shoes', 6: 'Books and Files'}
    return type_dict[num_type]


def convert_location_to_txt(location):
    locations = location.split(',')
    locations = [location.split('-')[-3] if len(location.split('-')) >= 3 else location.split('-')[-1]
                 for location in locations]
    # app.logger.info(locations)
    return '，'.join(locations)


def convert_location_to_xy(location):
    locations = location.split(',')
    app.logger.info(locations)
    coor_lst = [(float(location.split('-')[-2]), float(location.split('-')[-1])) if len(location.split('-')) >= 3 else None
                for location in locations]
    pixelcoor_lst = [convert_coor_to_pixelcoor(coor) for coor in coor_lst]
    app.logger.info(pixelcoor_lst)
    return pixelcoor_lst


def get_distance(lost_thing, pick_thing):
    lost_locations = convert_location_to_xy(lost_thing.location)
    pick_location = convert_location_to_xy(pick_thing.location)[0]
    min_distance = 30
    for lost_location in lost_locations:
        distance = math.sqrt((float(lost_location[0]) - float(pick_location[0])) ** 2 + (float(lost_location[1]) - float(pick_location[1])) ** 2)
        min_distance = distance if distance < min_distance else min_distance
    app.logger.info('min_distance')
    app.logger.info(min_distance)
    return min_distance


def get_notice_num(student):
    notice_num = 0
    for lost_thing in student.lostThings:
        if (lost_thing.status == 1):
            notice_num += 1
    for pick_thing in student.pickThings:
        if (pick_thing.status == 1):
            notice_num += 1
    return notice_num


def redirect_back(default='index', return_id='', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            if return_id:
                target += '#' + return_id
            return redirect(target)
    return redirect(default, **kwargs)


def check_date(lost_thing, pick_thing):
    if (lost_thing.lostDate and pick_thing.pickDate):
        return (lost_thing.lostDate.year <= pick_thing.pickDate.year or
                (lost_thing.lostDate.month <= pick_thing.pickDate.month and lost_thing.lostDate.year == pick_thing.pickDate.year)
                or (lost_thing.lostDate.year == pick_thing.pickDate.year and lost_thing.lostDate.month == pick_thing.pickDate.month
                    and lost_thing.lostDate.day <= pick_thing.pickDate.day))
    else:
        return 1


# database
match_table = db.Table('match_things', db.Column('lost_id', db.Integer, db.ForeignKey('lostThing.id')),
                       db.Column('pick_id', db.Integer, db.ForeignKey('pickThing.id')))


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
    __tablename__ = 'lostThing'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    name = db.Column(db.String(20))
    lostDate = db.Column(db.Date)
    contactPerson = db.Column(db.String(20))
    contactEmail = db.Column(db.String(40))
    location = db.Column(db.String(200))
    complement = db.Column(db.String(100))
    status = db.Column(db.Integer)  # 0 for waiting; 1 for matched; 2 for found
    lostStudent_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    match_pick_things = db.relationship('PickThing',
                                   secondary=match_table,
                                   back_populates='match_lost_things')
    confirm_pick_thing_id = db.Column(db.Integer)

    def __repr__(self):
        return '<LostThing %r>' % self.id


class PickThing(db.Model):
    __tablename__ = 'pickThing'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    name = db.Column(db.String(20))
    pickDate = db.Column(db.Date)
    contactPerson = db.Column(db.String(20))
    contactEmail = db.Column(db.String(40))
    location = db.Column(db.Integer)
    complement = db.Column(db.String(100))
    status = db.Column(db.Integer)  # 0 for waiting; 1 for matched; 2 for found
    pickStudent_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    match_lost_things = db.relationship('LostThing',
                                        secondary=match_table,
                                        back_populates='match_pick_things')
    confirm_lost_thing_id = db.Column(db.Integer)

    def __repr__(self):
        return '<PickThing %r>' % self.id


def check_login():
    if 'logged_in' not in session or not Student.query.get(session['login_user']):
        app.logger.info('fuck')
        return 0
    else:
        app.logger.info('shit')
        return 1


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if (not check_login()):
        return redirect(url_for('login'))
    student = Student.query.get(session['login_user'])
    notice_num = get_notice_num(student)
    num_per_page = 8
    all_lost_things = LostThing.query.all()
    all_not_found_lost_things = LostThing.query.filter(LostThing.status.in_([0, 1])).all()
    all_pick_things = PickThing.query.all()
    all_not_found_pick_things = PickThing.query.filter(PickThing.status.in_([0, 1])).all()
    return render_template('index.html',
                           student=student,
                           all_lost_things=all_lost_things,
                           all_pick_things=all_pick_things,
                           all_not_found_lost_things=all_not_found_lost_things,
                           all_not_found_pick_things=all_not_found_pick_things,
                           convert_type=convert_type,
                           convert_location_to_txt=convert_location_to_txt,
                           convert_location_to_xy=convert_location_to_xy,
                           int=int,
                           num_per_page=num_per_page,
                           lost_pages=math.ceil(len(all_not_found_lost_things)/num_per_page),
                           pick_pages=math.ceil(len(all_not_found_pick_things) / num_per_page),
                           notice_num=notice_num)


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
    if request.method == 'GET' and 'login_user' in session and Student.query.get(session['login_user']) and Student.query.filter_by(id=session['login_user']):
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


@app.route('/lost', methods=['GET', 'POST'])
def lost():
    if (not check_login()):
        return redirect(url_for('login'))
    lostForm = LostForm()
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    # if (request.method == 'POST'):
    #     lostInfo = request.form.to_dict()
    #     app.logger.info(lostInfo)
    #     (year, month, day) = lostInfo['lostDate'].split('-')
    #     date = datetime.date(int(year), int(month), int(day))
    #     app.logger.info(date.year)
    #     for loc in lostForm.lostLocation.data.split(','):
    #         app.logger.info(loc)
    student = Student.query.get(session['login_user'])
    notice_num = get_notice_num(student)
    if lostForm.validate_on_submit():
        app.logger.info('nb')
        date = None
        lost_info = request.form.to_dict()
        if (lost_info['lostDate'] != ''):
            (year, month, day) = lost_info['lostDate'].split('-')
            date = datetime.date(int(year), int(month), int(day))
        lost_thing = LostThing(
            type=lostForm.itemType.data,
            name=lostForm.itemName.data,
            lostDate=date,
            contactPerson=lostForm.contactPerson.data,
            contactEmail=lostForm.emailAddress.data,
            location=lostForm.lostLocation.data,
            complement=lostForm.complement.data,
            status=0,
            lostStudent_id=session['login_user']
        )
        db.session.add(lost_thing)
        for pick_thing in PickThing.query.filter_by(type=lost_thing.type).filter(PickThing.status.in_([0, 1])):
            app.logger.info(pick_thing)
            if (get_distance(lost_thing, pick_thing) <= 25 and check_date(lost_thing, pick_thing)):
                app.logger.info(pick_thing)
                lost_thing.status = 1
                pick_thing.status = 1
                lost_thing.match_pick_things.append(pick_thing)
                db.session.commit()
        db.session.commit()
        for thing in lost_thing.match_pick_things:
            app.logger.info(thing.name)
        return redirect(url_for('index'))
    return render_template('lost.html',
                           student=student,
                           form=lostForm,
                           notice_num=notice_num)


@app.route('/found', methods=['GET', 'POST'])
def found():
    if (not check_login()):
        return redirect(url_for('login'))
    foundForm = FoundForm()
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    # if (request.method == 'POST'):
    #     lostInfo = request.form.to_dict()
    #     app.logger.info(lostInfo)
    #     (year, month, day) = lostInfo['lostDate'].split('-')
    #     date = datetime.date(int(year), int(month), int(day))
    #     app.logger.info(date.year)
    #     for loc in lostForm.lostLocation.data.split(','):
    #         app.logger.info(loc)
    student = Student.query.get(session['login_user'])
    notice_num = get_notice_num(student)
    if foundForm.validate_on_submit():
        app.logger.info('nb')
        date = None
        pick_info = request.form.to_dict()
        if (pick_info['lostDate'] != ''):
            (year, month, day) = pick_info['lostDate'].split('-')
            date = datetime.date(int(year), int(month), int(day))
        pick_thing = PickThing(
            type=foundForm.itemType.data,
            name=foundForm.itemName.data,
            pickDate=date,
            contactPerson=foundForm.contactPerson.data,
            contactEmail=foundForm.emailAddress.data,
            location=foundForm.foundLocation.data,
            complement=foundForm.complement.data,
            status=0,
            pickStudent_id=session['login_user']
        )
        db.session.add(pick_thing)
        for lost_thing in LostThing.query.filter_by(type=pick_thing.type).filter(LostThing.status.in_([0, 1])):
            app.logger.info('ist')
            if (get_distance(lost_thing, pick_thing) <= 25 and check_date(lost_thing, pick_thing)):
                app.logger.info('was')
                lost_thing.status = 1
                pick_thing.status = 1
                pick_thing.match_lost_things.append(lost_thing)
                db.session.commit()
                # lost_thing.match_pick_things.append(pick_thing)
        db.session.commit()
        for thing in pick_thing.match_lost_things:
            app.logger.info(thing.name)
        return redirect(url_for('index'))
    return render_template('found.html',
                           student=student,
                           form=foundForm,
                           notice_num=notice_num)


@app.route('/personal_page')
def personal_page():
    if (not check_login()):
        return redirect(url_for('login'))
    student = Student.query.get(session['login_user'])
    personal_lost_things = student.lostThings
    personal_lost_things.sort(key=lambda thing:(thing.status, thing.id))
    personal_pick_things = student.pickThings
    personal_pick_things.sort(key=lambda thing: (thing.status, thing.id))
    return render_template('personal_page.html',
                           student=student,
                           personal_lost_things=personal_lost_things,
                           personal_pick_things=personal_pick_things,
                           convert_type=convert_type,
                           convert_location_to_txt=convert_location_to_txt,
                           str=str)


@app.route('/Terms_and_Conditions')
def Terms_and_Conditions():
    return '<h1>Surprise!</h1>'


@app.route('/match_things_found/<lost_thing_id>/<pick_thing_id>/<return_id>')
def match_things_found(lost_thing_id, pick_thing_id, return_id):
    lost_thing = LostThing.query.filter_by(id=lost_thing_id).first()
    pick_thing = PickThing.query.filter_by(id=pick_thing_id).first()
    lost_thing.status = pick_thing.status = 2
    app.logger.info('lost')
    m_pick_things = [thing for thing in lost_thing.match_pick_things]
    m_lost_things = [thing for thing in pick_thing.match_lost_things]
    for other_pick_thing in m_pick_things:
        if other_pick_thing.id != pick_thing.id:
            lost_thing.match_pick_things.remove(other_pick_thing)
            if len(other_pick_thing.match_lost_things) == 0:
                other_pick_thing.status = 0
    for other_lost_thing in m_lost_things:
        if other_lost_thing.id != lost_thing.id:
            pick_thing.match_lost_things.remove(other_lost_thing)
            if len(other_lost_thing.match_pick_things) == 0:
                other_lost_thing.status = 0
    db.session.commit()
    return redirect_back(return_id=return_id)


@app.route('/log_out')
def log_out():
    session.pop('logged_in')
    return redirect(url_for('login'))


@app.route('/drop_lost_thing/<id>')
def drop_lost_thing(id):
    app.logger.info(id)
    lost_thing = LostThing.query.get(int(id))
    app.logger.info(LostThing.query.all())
    if (lost_thing):
        student = Student.query.get(lost_thing.lostStudent_id)
        student.lostThings.remove(lost_thing)
        m_pick_things = [thing for thing in lost_thing.match_pick_things]
        for pick_thing in m_pick_things:
            pick_thing.match_lost_things.remove(lost_thing)
            if len(pick_thing.match_lost_things) == 0:
                pick_thing.status = 0
        db.session.delete(lost_thing)
        db.session.commit()
        app.logger.info('delete success')
    return redirect_back(return_id='A1')


@app.route('/drop_pick_thing/<id>')
def drop_pick_thing(id):
    app.logger.info(id)
    pick_thing = PickThing.query.get(int(id))
    app.logger.info(PickThing.query.all())
    if (pick_thing):
        student = Student.query.get(pick_thing.pickStudent_id)
        student.pickThings.remove(pick_thing)
        m_lost_things = [thing for thing in pick_thing.match_lost_things]
        for lost_thing in m_lost_things:
            lost_thing.match_pick_things.remove(pick_thing)
            if len(lost_thing.match_pick_things) == 0:
                lost_thing.status = 0
        db.session.delete(pick_thing)
        db.session.commit()
        app.logger.info('delete success')
    return redirect_back(return_id='A2')


@app.route('/remove_match_thing/<lost_thing_id>/<pick_thing_id>/<return_id>')
def remove_match_thing(lost_thing_id, pick_thing_id, return_id):
    lost_thing = LostThing.query.get(lost_thing_id)
    pick_thing = PickThing.query.get(pick_thing_id)
    if (lost_thing.confirm_pick_thing_id == pick_thing_id):
        lost_thing.confirm_pick_thing_id = None
    if (pick_thing.confirm_lost_thing_id == lost_thing_id):
        pick_thing.confirm_lost_thing_id = None
    lost_thing.match_pick_things.remove(pick_thing)
    if len(lost_thing.match_pick_things) == 0:
        lost_thing.status = 0
    if len(pick_thing.match_lost_things) == 0:
        pick_thing.status = 0
    db.session.commit()
    return redirect_back(return_id=return_id)


@app.route('/confirm_pick_thing/<lost_thing_id>/<pick_thing_id>/<return_id>')
def confirm_pick_thing(lost_thing_id, pick_thing_id, return_id):
    app.logger.info(lost_thing_id, pick_thing_id)
    lost_thing = LostThing.query.get(lost_thing_id)
    lost_thing.confirm_pick_thing_id = pick_thing_id
    db.session.commit()
    return redirect_back(return_id=return_id)


@app.route('/confirm_lost_thing/<lost_thing_id>/<pick_thing_id>/<return_id>')
def confirm_lost_thing(lost_thing_id, pick_thing_id, return_id):
    app.logger.info(lost_thing_id, pick_thing_id)
    pick_thing = PickThing.query.get(pick_thing_id)
    pick_thing.confirm_lost_thing_id = lost_thing_id
    db.session.commit()
    return redirect_back(return_id=return_id)


def checkRememberAndPop():
    if 'remember' in session:
        session.pop('remember')
