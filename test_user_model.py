"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        user1 = User.signup('user1', 'youremail@gmail.com', 'password', None)
        user2 = User.signup('user2', 'youreemail2@gmail.com', 'password', None)
        user1.id=1
        user2.id=2
        db.session.commit()

        self.user1 = user1
        self.user2 = user2
        self.user1.id = 1
        self.user2.id = 2

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        
    def test_follows(self):
        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertEqual(len(self.user1.following), 1)
        self.assertEquals(len(self.user2.followers), 1)
    def test_doesnt_follow(self):
        self.assertEqual(len(self.user1.following), 0)
    def test_create(self):
        self.assertTrue(self.user1)
    # def test_false_create(self):
    #     user_false_test = User.signup('test', None, 'password', None)
    #     user_false_test.id = 5
    #     with self.assertRaises(exc.IntegrityError) as context:
    #         db.session.commit()
    def test_authenticate(self):
        self.assertTrue(self.user1.username, self.user1.password)