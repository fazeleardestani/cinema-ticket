import uuid

import jdatetime

from utils import data_load, data_dump, str_to_datetime, str_to_showimg_datetime

FILE_PATH = 'data/showings.json'

class Movies:
    """A class to represent a movie with its details."""
    def __init__(self, name:str, age_group:int):
        """Initializes a new movie instance."""
        self.name = name
        self.age_group = age_group

class Showing:
    """A class to manage movie showings."""
    showings = data_load(FILE_PATH) or []
    def __init__(self, movie:Movies, showing_capacity:int, price:int, showing_time:str):
        """Initializes a new showing instance."""
        self.showing_id = str(uuid.uuid4())
        self.movie_name = movie.name
        self.movie_age_group = movie.age_group
        self.showing_capacity = showing_capacity
        self.showing_time = showing_time
        self.price = price
        self.reserved_seat = []

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the showing."""

        return f'Movie: {self.movie_name}, Show Capacity: {self.showing_capacity},Time: {self.showing_time}, Age Group:{self.movie_age_group} , Ticket Price:{self.price}'

    def to_dict(self)->dict:
        """Converts the showing object to a dictionary."""
        return {
            'id': self.showing_id,
            'name': self.movie_name,
            'age_group': self.movie_age_group,
            'showing_capacity': self.showing_capacity,
            'price': self.price,
            'showing_time': self.showing_time,
            'reserved_seat': self.reserved_seat
        }


    @classmethod
    def create_showing(cls, movie:Movies, showing_capacity:int, price:int , showing_time):
        """Creates a new showing, saves it, and returns the instance."""
        str_to_showimg_datetime(showing_time)
        showing = cls(movie, showing_capacity, price , showing_time)
        cls.showings.append(showing.to_dict())
        data_dump(FILE_PATH, cls.showings)
        return showing

    @classmethod
    def get_active_showings(cls):
        """Returns a list of active showings."""
        active_showings = []
        now = jdatetime.datetime.now()

        for showing in cls.showings:
            try:

                showing_time = str_to_showimg_datetime(showing['showing_time'])

                is_not_full = len(showing['reserved_seat']) < showing['showing_capacity']
                is_in_future = showing_time > now

                if is_not_full and is_in_future:
                    active_showings.append(showing)

            except Exception as e:
                print(e)

        return active_showings


    @classmethod
    def update_show(cls, self_showing):
        """ update user information in users list file."""
        for showing in cls.showings:
            if showing['id'] == self_showing.showing_id:
                showing['name'] = self_showing.movie_name
                showing['age_group'] = self_showing.movie_age_group
                showing['showing_capacity'] = self_showing.showing_capacity
                showing['price'] = self_showing.price
                showing['showing_time'] = self_showing.showing_time
                showing['reserved_seat'] = self_showing.reserved_seat

        data_dump(FILE_PATH, cls.showings)




