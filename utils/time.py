import datetime
from . import constants

def get_string_date(for_file = False, system_time = False):
    return get_string_format_date(constants.GENERAL_DATE_PATTERN if not for_file else constants.FILE_DATE_PATTERN, system_time)

def get_string_format_date(pattern, system_time = False):
    return datetime.datetime.strftime(datetime.datetime.utcnow() if not system_time else datetime.datetime.now(), pattern)

def get_utc_timestamp():
    return int(datetime.datetime.timestamp(datetime.datetime.utcnow()))

def get_system_timestamp():
    return int(datetime.datetime.timestamp(datetime.datetime.now()))

def to_timestamp(datetime_object):
    return int(datetime.datetime.timestamp(datetime_object))

def string_to_timestamp(string, pattern):
    return to_timestamp(datetime.datetime.strptime(string, pattern))

def github_date_string_to_timestamp(string):
    return string_to_timestamp(string, "%Y-%m-%dT%H:%M:%SZ")

def to_seconds(months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0):
    return int(datetime.timedelta(weeks = weeks,
                                  days = days,
                                  hours = hours,
                                  minutes = minutes,
                                  seconds = seconds).total_seconds())