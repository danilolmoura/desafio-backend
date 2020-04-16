from application.models import Trip
from application.models import User

def get_headers():
    header = {
        'Content-Type': 'application/json',
    }
    return header

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
    obj = Terminal(**kwargs)

    return insert_object(session, obj)
