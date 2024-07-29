import json
from graphene_django.utils.testing import GraphQLTestCase

from apps.auth.models import User
from test_utils.generators import create_user, create_users

from faker import Faker

fake = Faker()
Faker.seed(0)


class UserTestCases(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"

    def test_verify_username_availabile(self):
        # Create a number of users
        test_users = create_users(10)
        test_username = "test_user"

        response = self.query(
            '''
            mutation validateUsername($username: String!) {
                validateUsername(username: $username) {
                    success
                    error
                    valid
                }
            }
            ''',
            variables={
                "username": test_username
            }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        data = content["data"]["validateUsername"]

        self.assertTrue(data["valid"])

    def test_verify_username_unavailable(self):
        test_users = create_users(10)

        response = self.query(
            '''
            mutation validateUsername($username: String!) {
                validateUsername(username: $username) {
                    success
                    error
                    valid
                }
            }
            ''',
            variables={
                "username": test_users[3].username
            }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        data = content["data"]["validateUsername"]
        self.assertFalse(data["valid"])

    def test_retrieve_user_data(self):
        user = create_user()

        response = self.query(
            '''
            query user($username: String) {
                user(username: $username) {
                    id
                    name
                    username
                    password
                    email
                    firstName
                    lastName
                }
            }
            ''',
            variables={
                "username": user.username
            }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        user = content["data"]["user"]

        self.assertEqual(user.first_name, user["first_name"])

    def test_update_user_data(self):
        # Create a user

        # Call mutation to update user data

        # Retrieve user and verify it is changed
        pass

    def test_delete_account(self):
        # Create a user

        # Call mutation to delete the user

        # Retrieve with username and verify returns nothing
        pass
