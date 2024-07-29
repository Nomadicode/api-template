import json
from graphene_django.utils.testing import GraphQLTestCase

from test_utils.generators import create_continents


class ContinentTestCases(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        self.continents = create_continents(7)

    def test_fetch_all_continents(self):
        response = self.query(
            '''
            query continents {
                continents {
                    edges {
                        node {
                            id
                            name
                            isoCode
                        }
                    }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        all_continents = content["data"]["continents"]["edges"]

        self.assertEqual(len(self.continents), len(all_continents))

    def test_fetch_continent_by_code(self):
        response = self.query(
            '''
            query continents($isoCode_Iexact: String) {
                continents(isoCode_Iexact: $isoCode_Iexact) {
                    edges {
                        node {
                            id
                            name
                            isoCode
                        }
                    }
                }
            }
            ''',
            variables={
                "isoCode_Iexact": self.continents[2].iso_code
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        continent = content["data"]["continents"]["edges"]

        self.assertEqual(len(continent), 1)
        self.assertEqual(continent[0]["node"]["name"], self.continents[2].name)
