from flask import Flask, render_template
from flask import request 
from jinja2 import Template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

class NameForm(FlaskForm):
  name = StringField('What is your name?', validators=[DataRequired()])
  submit = SubmitField('Submit')

