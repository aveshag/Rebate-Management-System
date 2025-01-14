from datetime import datetime


def get_current_time():
    return datetime.now().replace(microsecond=0)
