import hashlib
import json
import re

from datetime import datetime

import jdatetime
from django.utils.formats import date_format

from custom_log import logger as log
from exeptions import InvalidDateError


def data_dump(file_path:str , data:list):
    """Saves a dictionary to a JSON file."""
    with open(file_path,'w') as file:
        json.dump(data, file, indent=4)

def data_load(file_path:str):
    """Loads a dictionary from a JSON file."""
    try:
        with open(file_path) as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []

def hash_password(password: str) -> str:
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode('utf8')).hexdigest()

def str_to_datetime(date:str):
    """
        Converts a date string in 'YYYY-M-D' or 'YYYY-MM-DD' format to a jdatetime object.
        Raises InvalidDateError if the format is incorrect.
        """
    date_format = "%Y-%m-%d"
    try:
        new_date = jdatetime.datetime.strptime(date, date_format)
        return new_date

    except (ValueError , TypeError):
        log.warning("Validation failed for date: '{}'. Format should be YYYY-M-D or YYYY-MM-DD.".format(date))
        raise InvalidDateError

def str_to_showimg_datetime(datetime_str:str):
    """Converts a showing datetime string ('YYYY-M-D HH:MM') to a jdatetime object."""
    datetime_format = "%Y-%m-%d %H:%M"
    try:
        new_datetime = jdatetime.datetime.strptime(datetime_str, datetime_format)
        return new_datetime
    except (ValueError , TypeError):
        log.warning(f"Validation failed for showing time: '{datetime_str}'. Format should be YYYY-M-D HH:MM.")
        raise InvalidDateError

def calculate_time_span(start:jdatetime.datetime , end:jdatetime.datetime):
    """
    Calculates the time difference (span) between two time.
    """
    time_span = end - start
    return time_span


def apply_discount(price:int , discount:int):
    discount_amount = int((price * discount)/100)
    return price - discount_amount
