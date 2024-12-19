from functools import wraps

from src.constants import SERVICE
from src.utils.session import get_session


def setup_db(settings):
    """Get or config current SQLAlchemy session."""

    def inner_function(function):
        @wraps(function)
        def wrapper(*args):
            db_settings = {**settings, "query": {"application_name": SERVICE}}
            get_session(**db_settings)
            return function(*args)

        return wrapper

    return inner_function
