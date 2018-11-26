rom flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..models import User, Pitch, Comments
from flask_login import login_required, current_user
from .. import db
import markdown2
from datetime import datetime
from .forms import PitchForm, CommentForm
from ..pitches import get_pitch

@main.route('/')
def index():
  posts=Posts.query.all()
  title = 'Welcome to Yucca'
  return render_template('index.html', title=title, posts=posts)

@main.route('/profile/<uname>/<id>')
@login_required
def profile(id, uname):
  admin = admin.query.filter_by(username = uname)
  posts = Posts.query.filter_by(id=id)
  message='You don\'t have any pitches to show you failure!'
  if posts is not 0:
    message='You\'ve got a few to show'
  if admin is None:
    abort(404)
  return render_template('profile/profile.html', admin=admin, posts=posts, message=message)

@main.route('/writing-post', methods=['GET', 'POST'])
@login_required
def write_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, body=form.body.data, category=form.category.data)

    db.session.add(pitch)
    db.session.commit()
    return redirect(url_for('main.index'))

  title = 'New Post'
  return render_template('new_post.html', post=form, title=title)

@main.route('/comment', methods=['GET', 'POST'])
def write_comment():
  form = CommentForm()
  if form.validate_on_submit():
    comment = Comments(comment=form.comment.data)
    comment.save_comment()

    return redirect(url_for('main.index'))

  return render_template('comment.html', comment=form)

@main.route('/snacks_and_drinks')
def get_snacks_and_drinks():
  posts = Posts.query.filter_by(category='san')
  title='Snacks and Drinks'
  message='There are no posts in the Snacks and drinks section. Go back to home to continue viewing.'
  if posts is not 0:
    message='Snacks and Drinks'
  return render_template('index.html', posts=posts, title=title, message=message)

@main.route('/sweets')
def get_sweets():
  posts = Posts.query.filter_by(category='swt')
  title='Sweets'
  message='There are no posts in the Sweetss section. Go back to home to continue viewing.'
  if pitches is not 0:
    message='Sweets'
  return render_template('index.html', posts=posts, title=title, message=message)

@main.route('/meals')
def get_meals():
  posts = Posts.query.filter_by(category='meals')
  title='Meals'
  message='There are no posts in the Meals section. Go back home to continue viewing.'
  if posts is not 0:
    message='Meals'
  return render_template('index.html', posts=posts, title=title, message=message)

@main.route('/conundrums')
def get_conundrums():
  posts = Posts.query.filter_by(category='con')
  title='Kitchen Conundrums'
  message='There are no posts in the Kitchen Conundrums section. Go back to home to continue viewing'
  if posts is not 0:
    message='Kitchen Conundrums'
  return render_template('index.html', posts=posts, title=title, message=message)

@main.route('/view-comments/<id>')
def view_comments(id):
  posts = Posts.query.filter_by(id=id)
  comments = Comments.query.filter_by(id=id)
  message='No comments'
  if comments is not 0:
    message=f'You\'re now viewing the comments. Click home to continue browsing'
  return render_template('index.html', message=message, comments=comments, posts=posts)

@main.route('/delete/<id>')
@login_required
def post_delete(id):
  posts = Posts.query.filter_by(id=id)
  return post.delete_post()