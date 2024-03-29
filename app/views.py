from flask import render_template,flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .models import User
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')
@login_required #确保登陆的用户才能看到
def index():
	user = g.user
	posts = [
	{
		'author':{'nickname':'John'},
		'body': 'Beatiful day in Portland!'
	},
	{
		'author':{'nickname':'Susan'},
		'body': 'The Avengers movie was so cool!'
	}
	]
	return render_template('index.html',
		title = 'Home',
		user = user,
		posts = posts)



@app.route('/login',methods=['GET', 'POST'])
@oid.loginhandler	#告诉flask-openid这是登陆函数
def login():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		return oid.try_login(form.openid.data,ask_for=['nickname', 'email'])
	return render_template('login.html', 
		title='Sign In', 
		form=form, 
		providers=app.config['OPENID_PROVIDERS'])


@app.before_request
def before_request():
	g.user = current_user


@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invaild_login, Please try again.')
		return redirect(url_for('login'))
	user = User.query.filter_by(email=resp.mail).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.emil.spilt('@')[0]
		user = User(nickname=nickname, email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember = remember_me)
	return redirect(request.args.get('next') or url_for('index'))
		

	# form =  LoginForm()
	# if form.validate_on_submit():
	# 	flash('Login requeseted for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
	# 	return redirect('index')
	# return render_template('login.html',
	# 	title="Sign In",
	# 	form = form,
	# 	providers = app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))