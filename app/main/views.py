from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from ..models import Admin, Posts, Comments
from flask_login import login_required, current_user
from .. import db,photos
import markdown2
from datetime import datetime
from .forms import PostForm, CommentForm
 

@main.route('/')
def index():
  posts=Posts.query.all()
  print(posts[0].title)
  # default_post=Posts(id=1, title='J', body='JJ', category='J', admin_id=1)
  # Posts.save_posts(default_post)
  print(posts)
  title = 'Welcome tto Yucca'
  return render_template('index.html', title=title, posts=posts, message='meh,i work')

@main.route('/profile/<uname>/<id>')
@login_required
def profile(id, uname):
  admin = Admin.query.filter_by(username = uname)
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
    filename = photos.save(request.files['photo_path'])
    path = f'photos/{filename}'
    posts = Posts(title=form.title.data, body=form.body.data, photo_path=path, category=form.category.data)

    db.session.add(posts)
    db.session.commit()
    return redirect(url_for('main.index'))

  title = 'New Post'
  return render_template('new_post.html', blog_form =form, title=title)

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
  if posts is not 0:
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

@main.route('/view_posts/<id>', methods=['GET','POST'])
def view_post(id):
  form = CommentForm()
  if form.validate_on_submit():
    comment = Comments(comment=form.comment.data)
    comment.save_comment()
    return redirect(url_for('main.view_post', id=id))

  posts = Posts.query.filter_by(id=id).first()
  comments = Comments.query.filter_by(id=id).all()
  message='No comments'
  if posts is not 0:
    message=f'You\'re now viewing the comments. Click home to continue browsing'
  return render_template('post.html', message=message, comments=comments, posts=posts, comment_form=form)

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
  return posts.delete_post()