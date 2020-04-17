import datetime
import json
import pdb

from dateutil.tz import tzlocal

from application.models import EnumBikeTripType

from . import test_utils

class TestTripResource():
    url_trip = '/api/v1/trip'
    url_trip_all = '/api/v1/trip/all'
    url_auth = '/auth'

    def test_get_all_trips(self, app, test_client, session, teardown):
        def should_return_all_trips_for_logged_user(app, test_client, session):
            # Create the user that will be used to test
            user = test_utils.create_user(
                session,
                name='Danilo da Silva Moura',
                password='12345',
                email='danilolmoura@gmail.com'
            )

            trip1 = test_utils.create_trip(
                session,
                classification=EnumBikeTripType.DESLOCAMENTO,
                start_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-31),
                end_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-30),
                score=5,
                user_id=user.id
            )

            trip2 = test_utils.create_trip(
                session,
                classification=EnumBikeTripType.DESLOCAMENTO,
                start_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-31),
                end_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-30),
                score=5,
                user_id=user.id
            )

            trip3 = test_utils.create_trip(
                session,
                classification=EnumBikeTripType.DESLOCAMENTO,
                start_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-31),
                end_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-30),
                score=4,
                user_id=user.id
            )

            trip4 = test_utils.create_trip(
                session,
                classification=EnumBikeTripType.DESLOCAMENTO,
                start_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-31),
                end_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-30),
                score=5,
                user_id=user.id
            )

            # Creates another User and Trip
            user2 = test_utils.create_user(
                session,
                name='Danilo da Silva Moura',
                password='12345',
                email='danilolmoura@gmail.com'
            )

            trip5 = test_utils.create_trip(
                session,
                classification=EnumBikeTripType.DESLOCAMENTO,
                start_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-31),
                end_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-30),
                score=5,
                user_id=user2.id
            )

            # Get the access token
            payload = json.dumps({
                'username': user.email,
                'password': user.password
            })
            res_login = test_client.post(
                self.url_auth,
                data=payload,
                headers=test_utils.get_headers()
            )
            token = json.loads(res_login.data)['access_token']

            # Access the endpoint
            res = test_client.get(
                self.url_trip_all,
                headers=test_utils.get_headers(token=token))

            trips = json.loads(res.data)
            assert len(trips) == 4

            for trip in trips:
                assert len(trip.keys()) == 5
                assert trip['id']
                assert trip['classificacao']
                assert trip['nota']
                assert datetime.datetime.strptime(
                    trip['data_inicio'], '%Y-%m-%dT%H:%M:%SZ')
                assert datetime.datetime.strptime(
                    trip['data_fim'], '%Y-%m-%dT%H:%M:%SZ')

        def should_return_an_empty_list_when_user_has_no_trips(app, test_client, session, teardown):
            # Create the user that will be used to test
            user = test_utils.create_user(
                session,
                name='Maria da Silva Moura',
                password='12345',
                email='maria@gmail.com'
            )

            payload = json.dumps({
                'username': user.email,
                'password': user.password
            })
            res_login = test_client.post(
                self.url_auth,
                data=payload,
                headers=test_utils.get_headers()
            )

            token = json.loads(res_login.data)['access_token']

            res = test_client.get(
                self.url_trip_all,
                headers=test_utils.get_headers(token=token))


            trips = json.loads(res.data)
            assert trips == []

        should_return_all_trips_for_logged_user(app, test_client, session)
        should_return_an_empty_list_when_user_has_no_trips(app, test_client, session, teardown)