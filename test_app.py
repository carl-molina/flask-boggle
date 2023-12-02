from unittest import TestCase

from app import app, games
from boggle import BoggleGame

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    # original location of setUp:
    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

        game = BoggleGame(board_size=3)

        game.board = [['Z', 'D', 'Z'],
                      ['Z', 'O', 'Z'],
                      ['Z', 'G', 'Z']]

        games['12345'] = game

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
        """Test starting a new game.
        Tests whether response is JSON string;
        Tests whether value of "game_id" is instance of str class;
        Tests whether value of "board" is instance of list class;
        Tests whether each board in board list is instance of list class;
        Tests whether game_id is in games dictionary."""

        with app.test_client() as client:
            response = client.post('/api/new-game')

            json = response.json

            self.assertEqual(response.is_json, True)
            self.assertIsInstance(json["game_id"], str)
            self.assertIsInstance(json["board"], list)

            for board in json["board"]:
                self.assertIsInstance(board, list)

            self.assertIn(json["game_id"], games)

    def test_api_score_word(self):
        """Tests whether word is a valid word on the board
        Tests "ZZZ" as a non-word
        Tests "PIG" as a word not-on-board
        Tests "DOG" as a word on board and valid word"
        Relies on setUp() function to build test board
        """

        with app.test_client() as client:
            resp1 = client.post('/api/score-word',
                                json={'game_id': '12345', "word": "ZZZ"})
            print('This is resp1', resp1)

            resp2 = client.post('/api/score-word',
                                json={'game_id': '12345', "word": "PIG"})
            print('This is resp2', resp2)

            resp3 = client.post('/api/score-word',
                                json={'game_id': '12345', "word": "DOG"})
            print('This is resp3', resp3)

            resp_json1 = resp1.get_json()
            self.assertEqual(resp_json1, {"result": "not-word"})

            resp_json2 = resp2.get_json()
            self.assertEqual(resp_json2, {"result": "not-on-board"})

            resp_json3 = resp3.get_json()
            self.assertEqual(resp_json3, {"result": "ok"})

            # set up a response as data
            # set up multiple responses
                # response 1 is not valid word
                # response 2 is valid but on board
                # response 3 is valid and on the board

        # TODO: tests whether word is a valid word
            # TODO: tests that response is JSON
        # TODO: tests whether word is a valid word in the dictionary
            # TODO: tests that response is JSON
        # TODO: tests whether word is on board
            # TODO: tests that response is JSON