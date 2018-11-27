from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import login_manager

@login_manager.user_loader
def load_admin(admin_id):
  return Admin.query.get(int(admin_id))

class Admin(UserMixin, db.Model):
  __tablename__='admin'

  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(255))
  email = db.Column(db.String(255))
  first_name = db.Column(db.String(255))
  surname = db.Column(db.String(255))
  pass_secure = db.Column(db.String(255))
  
  comments = db.relationship('Comments', backref='comments', lazy='dynamic')
  posts = db.relationship('Posts', backref='posts', lazy='dynamic')

  @property
  def password(self):
    raise AttributeError('You do not have the permissions to view password attribute')
  
  @password.setter
  def password(self, password):
    self.pass_secure = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.pass_secure, password)

  def save_admin(self):
    db.session.add(self)
    db.session.commit()

  def __repr__(self):
    return f'Admin {self.username}'


class Comments(db.Model):
  __tablename__='comments'

  id = db.Column(db.Integer, primary_key = True)
  comment = db.Column(db.String)
  admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  post = db.Column(db.Integer, db.ForeignKey('posts.id'))

  def save_comment(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_comments(cls, id):
    comments = Comments.query.filter_by(posts_id=id).all()
    return comments

class Posts(db.Model):
  __tablename__='posts'

  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(255))
  body = db.Column(db.String)
  photo_path = db.Column(db.String(255))
  posted = db.Column(db.DateTime,default=datetime.utcnow)
  category = db.Column(db.String)
  admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

  comments = db.relationship('Comments', backref='post_comments', lazy='dynamic')

  def save_posts(self):
    db.session.add(self)
    db.session.commit()

  @classmethod
  def get_posts(cls, id):
    posts = Posts.query.filter_by(category_id=id).all()
    return posts

  def get_comments(self):
    posts = Posts.query.filter_by(id = self.id).first()
    comments = Comments.query.filter_by(posts=posts.id)
    return comments