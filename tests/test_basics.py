import unittest
from flask import current_app
from app import create_app, db
from app.models import Permissions, Role, User, AnonymousUser

class BasicsTestBase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('tst')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
    def test_roles_and_permissions(self):
        Role.insert_roles()
        usr = User(username='test1', password='test1')
        self.assertTrue(usr.can(Permissions.WRITE_ARTICLES))
        self.assertFalse(usr.can(Permissions.MODERATE_COMMENTS))

        usr = User.query.filter_by(username='huxy').first()
        self.assertTrue(usr is not None)
        self.assertTrue(usr.is_administrator)

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permissions.FOLLOW))
