import unittest

from models.cinema import Showing, Movies


class TestCinemaModel(unittest.TestCase):
    def setUp(self):
        self.original_showings = Showing.showings
        Showing.showings = []

        self.movie = Movies('Inception' , 17)
        self.test_showing = Showing.create_showing(self.movie , 80 , 20, "1404-06-16 22:00")

    def tearDown(self):
        Showing.showings = self.original_showings

    def test_create_showing_succeeds(self):
        self.assertEqual(self.test_showing.movie_name, 'Inception')
        self.assertEqual(len(Showing.showings) , 1)

    def test_get_active_showings_returns_only_future_shows(self):
        deactive_showing = Showing.create_showing(self.movie, 80, 20, "1404-05-16 22:00")
        active_showings = self.test_showing.get_active_showings()
        self.assertEqual(len(active_showings), 1)

    def test_get_active_showings_excludes_full_shows(self):
        deactive_showing = Showing.create_showing(self.movie, 1, 20, "1404-06-16 22:00")
        deactive_showing.reserved_seat.append("uid")
        active_showings = self.test_showing.get_active_showings()
        self.assertEqual(len(active_showings), 1)