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
@login_required
def index():
  pitches=Pitch.query.all()
  title = 'Welcome to Jitches'
  return render_template('index.html', title=title, pitches=pitches)

@main.route('/profile/<uname>/<id>')
def profile(id, uname):
  user = User.query.filter_by(username = uname)
  pitches = Pitch.query.filter_by(id=id)
  message='You don\'t have any pitches to show you failure!'
  if pitches is not 0:
    message='You\'ve got a few to show'
  if user is None:
    abort(404)
  return render_template('profile/profile.html', user=user, pitches=pitches, message=message)

@main.route('/writing-pitch', methods=['GET', 'POST'])
@login_required
def write_pitch():
  form = PitchForm()
  if form.validate_on_submit():
    pitch = Pitch(title=form.title.data, body=form.body.data, category=form.category.data)

    db.session.add(pitch)
    db.session.commit()
    return redirect(url_for('main.index'))

  title = 'New Pitch'
  return render_template('new_pitch.html', pitch=form, title=title)

@main.route('/comment', methods=['GET', 'POST'])
@login_required
def write_comment():
  form = CommentForm()
  if form.validate_on_submit():
    comment = Comments(comment=form.comment.data)
    comment.save_comment()

    return redirect(url_for('main.index'))

  return render_template('comment.html', comment=form)

@main.route('/business')
def get_business():
  pitches = Pitch.query.filter_by(category='bus')
  title='Jitches Business Edition'
  message='There are no pitches in the Business section. Go back to home to continue viewing.'
  if pitches is not 0:
    message='Home of Business pitches'
  return render_template('index.html', pitches=pitches, title=title, message=message)

@main.route('/sports')
def get_sports():
  pitches = Pitch.query.filter_by(category='spr')
  title='Jitches Sports Edition'
  message='There are no pitches in the Sports section. Go back to home to continue viewing.'
  if pitches is not 0:
    message='Home of Sports pitches'
  return render_template('index.html', pitches=pitches, title=title, message=message)

@main.route('/technology')
def get_technology():
  pitches = Pitch.query.filter_by(category='tech')
  title='Jitches Tech Edition'
  message='There are no pitches in the Tech section. Go back home to continue viewing.'
  if pitches is not 0:
    message='Home of Tech pitches'
  return render_template('index.html', pitches=pitches, title=title, message=message)

@main.route('/misc')
def get_misc():
  pitches = Pitch.query.filter_by(category='misc')
  title='Jitches Misc. Edition'
  message='There are no pitches in the Misc. section. Go back to home to continue viewing'
  if pitches is not 0:
    message='Home of Misc. pitches'
  return render_template('index.html', pitches=pitches, title=title, message=message)

@main.route('/view-comments/<id>')
def view_comments(id):
  pitch = Pitch.query.filter_by(id=id)
  comments = Comments.query.filter_by(id=id)
  message='This pathetic pitch has no comments'
  if comments is not 0:
    message=f'You\'re now viewing the comments. Click home to continue browsing pitches'
  return render_template('comments.html', message=message, comments=comments, pitch=pitch)

@main.route('/delete/<id>')
def pitch_delete(id):
  pitch = Pitch.query.filter_by(id=id)
  return pitch.delete_pitch()