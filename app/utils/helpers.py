import datetime
from utils import constants


def is_valid_datetime(start_time, end_time):
    #TODO: Move the function to utils file.
    resturant_open_time = constants.RESTAURANT_OPEN_TIME
    resturant_close_time = constants.RESTAURANT_CLOSE_TIME

    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
    datetime_now = datetime.datetime.now()

    if end_time < start_time:
        return False
    elif (end_time < datetime_now) or (start_time < datetime_now):
        return False
    elif start_time.date() != end_time.date():
        return False
    elif (start_time.time() > resturant_close_time) or (start_time.time() < resturant_open_time):
        return False
    elif (end_time.time() > resturant_close_time) or (end_time.time() < resturant_open_time):
        return False
    return True