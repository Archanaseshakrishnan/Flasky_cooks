from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask import current_app
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin

class Role(db.Model):
  __tablename__ = 'roles'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), unique=True)
  users = db.relationship('User', backref='role')
  
  def __repr__(self):
    return '<Role %d,%r>' % (self.id,self.name)

class User(db.Model, UserMixin):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64), unique=True, index=True)
  username = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String(128))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  confirmed = db.Column(db.Boolean, default=False)
  
  @property
  def password(self):
    raise AttributeError('password not readable')
  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)
  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)
  def generate_confirmation_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expiration)
    return s.dumps({'confirm':self.id}).decode('utf-8')
  def confirm(self, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token.encode('utf-8'))
    except:
      return False
    self.confirmed = True
    db.session.add(self)
    return True
  def __repr__(self):
    return '<User  %d,%r,%s>' % (self.id,self.username,self.email)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))
  

