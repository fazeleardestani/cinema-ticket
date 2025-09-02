from utils import data_load, data_dump

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
    def __init__(self, movie:Movies, showing_capacity:int, price:int):
        """Initializes a new showing instance."""
        self.movie_name = movie.name
        self.movie_age_group = movie.age_group
        self.showing_capacity = showing_capacity
        self.price = price
        self.reserved_seat = []

    def __str__(self) -> str:
        """Returns a user-friendly string representation of the showing."""
        return f'Movie: {self.movie_name}, Show Capacity: {self.showing_capacity}, Ticket Price:{self.price}'

    def to_dict(self)->dict:
        """Converts the showing object to a dictionary."""
        return {
            'name': self.movie_name,
            'age_group': self.movie_age_group,
            'showing_capacity': self.showing_capacity,
            'price': self.price,
            'reserved_seat': self.reserved_seat
        }

    @classmethod
    def create_showing(cls, movie:Movies, showing_capacity:int, price:int):
        """Creates a new showing, saves it, and returns the instance."""
        showing = cls(movie, showing_capacity, price)
        cls.showings.append(showing.to_dict())
        data_dump(FILE_PATH, cls.showings)
        return showing
