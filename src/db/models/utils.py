from datetime import datetime


def get_current_time():
    """Get current time in UTC."""
    return datetime.now().replace(microsecond=0)
