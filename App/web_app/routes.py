from flask import render_template, flash, redirect, url_for, request, session
from web_app import app, db
from web_app.forms import LoginForm, RegistrationForm
from web_app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from web_app.token import generate_token, verify_token
from web_app.__init__ import publisher

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.query.filter_by(id=current_user.get_id()).first()
    if not user.is_authenticated or not user.verified:
        return redirect(url_for('login'))
    posts = [
            {
                'author': {'username': 'John'},
                'body': 'Beautiful day in Port!'
            },
            {
                'author': {'username': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }]
    return render_template('index.html', user=user, title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.verified:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        if not user.verified:
            flash('Please verify your email first')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    verified = False)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        #THIS bike is POWERFUL but terrifying
        login_user(user)
        return redirect(url_for('verify_email'))

    return render_template('register.html', title='Register', form=form)

@app.route('/verify/<token>', methods=['GET', 'POST'])
def verify(token):
    email = verify_token(token)
    if email=="":
        flash('The verification link is invalid or has expired.')
        return redirect(url_for('login'))


    user=User.query.filter_by(email=email).first()

    if user is None:
        flash("W-w-w-waaaaaaait")
        return redirect(url_for('login'))

    if user.verified:
        flash('Account already verified.')
    else:
        user.verified = True
        db.session.add(user)
        db.session.commit()
        flash('You have verified your account.')
    return redirect(url_for('login'))

@app.route('/verify_email')
def verify_email():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if current_user.is_authenticated and current_user.verified:
        return redirect(url_for('index'))
    user = User.query.filter_by(id=current_user.get_id()).first()

    token = generate_token(user.email)
    verification_url = url_for('verify', token=token, _external=True)
    sender = app.config['DEFAULT_MAIL_SENDER']
    pwd = app.config['MAIL_PASSWORD']
    publisher.publish_task(sender,pwd,"ver",user.email, verification_url)

    return render_template('verify_email.html', user=user, title='Email verification')
