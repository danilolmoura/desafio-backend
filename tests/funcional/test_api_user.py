import datetime
import json
import pdb

from application.models import User

from . import test_utils

class TestAuth():
    url_auth = '/auth'

    def test_get_access_token(self, app, test_client, session, teardown):
        def should_return_access_for_user_token(app, test_client, session):
            # Create the user that will be used to test
            user = test_utils.create_user(
                session,
                name='Danilo da Silva Moura',
                password='12345',
                email='danilolmoura@gmail.com'
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
            assert res_login.status_code == 200
            assert token

        should_return_access_for_user_token(app, test_client, session)
