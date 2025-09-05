import argparse
import getpass
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from custom_log import logger as log
from exeptions import InvalidAccess
from models.cinema import Showing, Movies
from models.user import User, UserRole


def admin_login()-> User | None:
    """Handles admin login and role verification."""
    os.system('cls')
    print("---Admin Login---")

    username = input("Admin Username: ")
    password = getpass.getpass("Admin Password: ")

    logged_in_admin = User.login(username, password)
    if logged_in_admin.role == UserRole.ADMIN:
        print('Welcome Admin')
        return logged_in_admin
    else:
        log.warning("Access Denied: This user is not an admin.")
        raise InvalidAccess

parser = argparse.ArgumentParser(description='Cinema Ticket Management')

parser.add_argument('--movie-title' , type=str, help='Movie Title' , required=True)
parser.add_argument('--time' , type=str, help='Showing time in "YYYY-M-D HH:MM" format' , required=True)
parser.add_argument('--capacity' , type=int, help='Total number of seats' , required=True)
parser.add_argument('--age-group' , type=int, help='Minimum age for the movie' , required=True)
parser.add_argument('--price' , type=int, help='Ticket price' , required=True)

args = parser.parse_args()

try:
    admin_login()

    print(f"Creating showing for movie: {args.movie_title}")
    print(f"Time: {args.time}")
    print(f"Capacity: {args.capacity}")
    print(f"Age Group: {args.age_group}")
    print(f"Price: {args.price}")

    movie = Movies(args.movie_title , args.age_group)
    Showing.create_showing(movie, args.capacity, args.price , args.time)
    print("\nShowing created successfully!")
except Exception as e:
    print(e)

