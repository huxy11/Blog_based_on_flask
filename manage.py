import os
from app import create_app, db
from app.models import User, Role, Comment, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

#parameter could be dft, dev, tst, prd
app = create_app('dft')
manager = Manager(app)
migrate = Migrate(app, db)

def msc():
    return dict(app = app, db = db, User = User, Role = Role, Comment = Comment, Post = Post)

@manager.command
def add_admin():
    user = User.query.filter_by(username='huxy').first()
    if not user:
        user = User(username='huxy',password='huxy')
        db.session.add(user)
        db.session.commit()
    
@manager.command
def deploy():
    """Run deplovment settings."""
    from flask_migrate import upgrade
    upgrade()
    Role.insert_roles()
    User.self_follow()

@manager.command
def test():
    """Running unit tests..."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command("shell", Shell(make_context = msc))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
