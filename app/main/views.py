from datetime import datetime
from flask import redirect, session, url_for, render_template
from . import main
from . import forms 
from .. import db
from ..models import User, Role
from ..email import send_email
from flask import redirect, session, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from config import config

@main.route('/', methods=['GET', 'POST'])
def index():
  form = forms.NameForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.name.data).first()
    if user is None:
      user = User(username=form.name.data)
      db.session.add(user)
      #db.session.commit()
      session['known'] = False
      flash('Welcome New User')
      #conf = config.Config()
      #if conf.FLASKY_ADMIN:
        #send_email(conf.FLASKY_ADMIN, 'New User', 'mail/new_user', user=user)
    else:
      session['known'] = True
      flash('Welcome Returning User')
    old_name = session.get('name')
    if old_name is not None and old_name != form.name.data:
      flash('Looks like you have changed your name!')
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('.index'))
  return render_template('index.html',form=form,name=session.get('name'), known=session.get('known',False), current_time=datetime.utcnow())
