from flask_potion import fields, ModelResource
from flask_potion.routes import ItemRoute, Route
from flask_jwt import jwt_required, current_identity
from werkzeug.exceptions import Forbidden

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

    @Route.GET('/all')
    @jwt_required()
    def all(self):
        """List all trips of an User

        Returns:
            list(dict): List of dicts, where each item on the list
                has information for each trip of the logged in user
        """

        trips = Trip.query.filter_by(
            user_id=current_identity.id
        ).order_by(
            Trip.id.desc()
        ).all()

        result_trips = []
        for trip in trips:
            trip_info = {
                'id': trip.id,
                'data_inicio': trip.start_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'data_fim': trip.end_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                'classificacao': trip.classification,
                'nota': trip.score
            }

            result_trips.append(trip_info)

        return result_trips

    @ItemRoute.POST('/rate_trip')
    @jwt_required()
    def rate_trip(
        self,
        trip,
        classification: fields.Integer(nullable=False),
        score: fields.Integer(nullable=False)):
        """List all trips of an User

        Returns:
            boolean: True if values are set correctly
        """

        if trip.user_id != current_identity.id:
            raise Forbidden(
                'You are not allowed to rate this trip')

        trip.classification = classification
        trip.score = score

        db.session.add(trip)
        try:
            db.session.commit()
        except Exception as e:
            logger.exception(e)
            db.session.rollback()

        return True

def create_api(api):
    api.add_resource(TripResource)
