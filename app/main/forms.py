from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import Required

class PitchForm(FlaskForm):
  title=StringField('Pitch Title')
  body=TextAreaField('Project Pitch')
  author=TextAreaField('Your name as it\'ll be displayed')
  category=SelectField('Category', choices=[('bus', 'Business'), ('tech', 'Technology'), ('spr', 'Sports'), ('misc', 'Misc.')])
  submit=SubmitField('Submit')

class UpdateProfile(FlaskForm):
  add_info=StringField('Your LinkedIn Profile')
  submit=SubmitField('Submit')

class CommentForm(FlaskForm):
  comment=StringField('Your comment:')
  submit=SubmitField('Post')