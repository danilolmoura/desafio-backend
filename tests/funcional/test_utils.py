from application.models import Trip
from application.models import User

def get_headers(token=None):
    headers = {
        'Content-Type': 'application/json'
    }

    if token:
        headers['Authorization'] = 'JWT {}'.format(token)

    return headers

def insert_object(session, obj):
    try:
        session.add(obj)
        session.commit()
        return obj
    except Exception as e:
        session.rollback()
        raise e

def create_trip(session, **kwargs):
    obj = Trip(**kwargs)

    return insert_object(session, obj)

def create_user(session, **kwargs):
    obj = User(**kwargs)

    return insert_object(session, obj)
