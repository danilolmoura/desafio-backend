import datetime
import json
import pdb

from dateutil.tz import tzlocal

from application.models import EnumBikeTripType, Trip

from . import test_utils

class TestTripResource():
    url_auth = '/auth'
    url_trip = '/api/v1/trip'
    url_trip_all = '/api/v1/trip/all'
    url_trip_rate_trip = '/api/v1/trip/{}/rate_trip'

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

    def test_rate_trip(self, app, test_client, session, teardown):
        def should_set_trip_rate(app, test_client, session):
            # Create the user that will be used to test
            user = test_utils.create_user(
                session,
                name='Danilo da Silva Moura',
                password='12345',
                email='danilolmoura@gmail.com'
            )

            trip = test_utils.create_trip(
                session,
                start_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-31),
                end_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-30),
                user_id=user.id
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

            # Set the score
            payload = json.dumps({
                'score': 5,
                'classification': EnumBikeTripType.DESLOCAMENTO,
            })

            res = test_client.post(
                self.url_trip_rate_trip.format(trip.id),
                data=payload,
                headers=test_utils.get_headers(token=token))

            result = json.loads(res.data)
            assert result == True

            trip = session.query(Trip).get(trip.id)

        def should_raise_forbidden_when_user_tries_to_rate_another_user_trip(
                app, test_client, session):
            # Create the user that will be used to test
            user = test_utils.create_user(
                session,
                name='Danilo da Silva Moura',
                password='12345',
                email='danilolmoura@gmail.com'
            )

            trip = test_utils.create_trip(
                session,
                start_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-31),
                end_date=datetime.datetime.now(
                    tzlocal()) + datetime.timedelta(days=-30),
                user_id=user.id
            )

            # Create another user without trip
            user2 = test_utils.create_user(
                session,
                name='Maria da Silva Moura',
                password='12345',
                email='maria@gmail.com'
            )

            # Get the access token for User2
            payload = json.dumps({
                'username': user2.email,
                'password': user2.password
            })
            res_login = test_client.post(
                self.url_auth,
                data=payload,
                headers=test_utils.get_headers()
            )
            token = json.loads(res_login.data)['access_token']

            # Tries to set score for another user trip
            payload = json.dumps({
                'score': 5,
                'classification': EnumBikeTripType.DESLOCAMENTO,
            })

            res = test_client.post(
                self.url_trip_rate_trip.format(trip.id),
                data=payload,
                headers=test_utils.get_headers(token=token))

            result = json.loads(res.data)
            assert res.status_code == 403

        should_set_trip_rate(app, test_client, session)
        should_raise_forbidden_when_user_tries_to_rate_another_user_trip(
            app, test_client, session)