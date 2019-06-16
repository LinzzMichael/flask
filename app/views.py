from flask import render_template,flash, redirect
from app import app
from .forms import LoginForm


@app.route('/')
@app.route('/index')

def index():
	user = { 'nickname': 'Miguel'}
	posts = [
	{
		'author':{'nickname': 'John'},
		'body': 'Beatiful day in Portland!'
	},
	{
		'author':{'nickname': 'Susan'},
		'body': 'The Avenger movies was so cool!'
	}
	]
	return render_template("index.html",
		title = "Home",
		posts = posts,
		user = user)



@app.route('/login',methods=['GET', 'POST'])
def login():
	form =  LoginForm()
	if form.validate_on_submit():
		flash('Login requeseted for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
		return redirect('index')
	return render_template('login.html',
		title="Sign In",
		form = form,
		providers = app.config['OPENID_PROVIDERS'])