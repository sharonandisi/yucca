from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, IntegerField, SelectField
from wtforms.validators import Required

class PostForm(FlaskForm):
  title=StringField('Post Title')
  body=TextAreaField('Blog Post')
  photo_path = FileField('post photo')
  author=TextAreaField('Your name as it\'ll be displayed')
  category=SelectField('Category', choices=[('san', 'Snack_and_Drinks'), ('Sweets', 'swt'), ('meals', 'meals'), ('con', 'conundrums')])
  submit=SubmitField('Submit')

class UpdateProfile(FlaskForm):
  add_info=StringField('Your Profile')
  submit=SubmitField('Submit')

class CommentForm(FlaskForm):
  comment=StringField('Your comment:')
  submit=SubmitField('Post')