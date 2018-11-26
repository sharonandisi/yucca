
from .models import Posts

def get_post(id):
  posts = Posts.query.filter_by(id=id)
  return posts