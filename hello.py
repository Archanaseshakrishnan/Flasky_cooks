#!/usr/bin/python
from flask import Flask, render_template
from flask import request 
from flask import redirect, session, url_for, flash
from flask import abort
from jinja2 import Environment, FileSystemLoader
from jinja2 import Template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'archana_hard_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <archanaseshakrishnan94@gmail.com>'
app.config['FLASKY_ADMIN'] = 'aseshakr@asu.edu'
bootstrap = Bootstrap(app)
template_dir = '/home/archana/flasky/templates'
env = Environment(loader=FileSystemLoader(template_dir))
argument = ["archu","deepoo","seshu"]

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

@app.shell_context_processor
def make_shell_context():
	return dict(db=db, User=User, Role=Role)

def send_async_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(to, subject, template, **kwargs):
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'],
	recipients=[to])
	msg.body = "This is a test message!"
	msg.html = "Flasky testing <b> Archu </b>"
	thr = Thread(target=send_async_email, args=[app,msg])
	thr.start()
	return thr

#static routing
@app.route('/', methods=['GET','POST'])
def index():
	form = NameForm() 
	user_agent = request.headers.get('User-Agent')
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			#db.session.commit()
			session['known'] = False
                        #flash('Welcome New User')
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
		else:
			session['known'] = True
			#flash('Welcome Returning User')
		old_name = session.get('name')
		if old_name is not None and old_name != form.name.data:
			flash('Looks like you have changed your name!')
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	# return '<h1>Testing!</h1><br><p> Your browser is {}</p>'.format(user_agent)
	return render_template('index.html',form=form,name=session.get('name'), known=session.get('known',False))
	# return redirect('www.google.com')

#dynamic routing - displays name dynamically
@app.route('/user/<name>')
def user(name):
	# return '<h1>Hello, {}!</h1>'.format(name)
	return render_template('user.html', name=name)

@app.route('/comments')
def trigger_comment():
	return render_template('comments.html', cmts=argument)

#app.route('/user/<id_>')
#def get_user(id_):
	#user = load_user(id_)
	#if not user:
		#abort(404)
	#return '<h1>Hello, {}!</h1>'.format(name)

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')
	def __repr__(self):
		return '<Role %d,%r>' % (self.id,self.name)

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	def __repr__(self):
		return '<User  %d,%r>' % (self.id,self.username)

if __name__ == '__main__':
	app.run()
