
from .models import Pitch

def get_pitch(id):
  pitches = Pitch.query.filter_by(id=id)
  return pitches