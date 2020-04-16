from flask_potion import ModelResource

from application import db
from application.models import Trip, User, EnumBikeTripType


class TripResource(ModelResource):
    class Meta:
        include_id = True
        model = Trip
        name = 'trip'
        exclude_fields = ['created_at']

    class Schema:
        pass


class UserResource(ModelResource):
    class Meta:
        include_id = True
        model = User
        name = 'user'
        exclude_fields = ['created_at']

    class Schema:
        pass


def create_api(api):
    api.add_resource(UserResource)
    api.add_resource(TripResource)
