from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            # Be careful on specificity of tests and make sure html really is
            # unique to the homepage. CAN TEST FOR COMMENTS!
            self.assertIn('<!-- Test: Homepage -->', html)
            self.assertIn('<script src="/static/boggle.js">', html)

            # FIXME: where/what is the session/in the session?

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            response = client.get('/api/new-game')

            json = response.get_json()

            #Test if return is json
            #Test if json is made up of string and list of list
            #Test if games dictionary increased by 1

