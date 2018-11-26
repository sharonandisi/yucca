from app import create_app, db
from app.models import Admin, Comments, Posts
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('production')

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)

@manager.command
def test():
  import unittest
  tests = unittest.TestLoader().discover('tests')

@manager.shell
def make_shell_context():
  return dict(app=app, db=db, Admin=Admin, Comments=Comments, Posts=Posts)

if __name__=='__main__':
  manager.run()