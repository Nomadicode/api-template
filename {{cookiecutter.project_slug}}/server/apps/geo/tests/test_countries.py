import json
from graphene_django.utils.testing import GraphQLTestCase

from test_utils.generators import create_continents, create_countries


class CountryTestCases(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        self.continents = create_continents(3)

        self.countries = []
        for continent in self.continents:
            self.countries += create_countries(10, continent=continent)

    def test_fetch_all_countries(self):
        response = self.query(
            '''
            query countries {
                countries {
                    edges {
                        node {
                            id
                            name
                            isoCode2
                            isoCode3
                        }
                    }
                }
            }
            '''
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        all_countries = content["data"]["countries"]["edges"]

        self.assertEqual(len(self.countries), len(all_countries))

    def test_fetch_countries_by_continent_code(self):
        response = self.query(
            '''
            query countries($continent_IsoCode_Iexact: String) {
                countries(continent_IsoCode_Iexact: $continent_IsoCode_Iexact) {
                    edges {
                        node {
                            id
                            name
                            isoCode2
                        }
                    }
                }
            }
            ''',
            variables={
                "continent_IsoCode_Iexact": self.continents[2].iso_code
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        countries = content["data"]["countries"]["edges"]

        self.assertEqual(10, len(countries))

    def test_fetch_country_by_code(self):
        response = self.query(
            '''
            query country($isoCode2: String) {
                country(isoCode2: $isoCode2) {
                    id
                    name
                    isoCode2
                }
            }
            ''',
            variables={
                "isoCode2": self.countries[2].iso_code_2
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        country = content["data"]["country"]

        self.assertEqual(self.countries[2].name, country["name"])
