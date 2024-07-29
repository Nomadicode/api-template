import json
from graphene_django.utils.testing import GraphQLTestCase

from test_utils.generators import create_continents, create_countries, create_regions


class RegionTestCases(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"

    def setUp(self):
        self.continents = create_continents(3)

        self.countries = []
        for continent in self.continents:
            self.countries += create_countries(10, continent=continent)

        self.regions = create_regions(5, country=self.countries[4])

    def test_fetch_all_regions_country(self):
        response = self.query(
            '''
            query regions ($country_IsoCode2_Iexact: String) {
                regions(country_IsoCode2_Iexact: $country_IsoCode2_Iexact) {
                    edges {
                        node {
                            id
                            name
                            isoCode
                            country {
                                isoCode2
                            }
                        }
                    }
                }
            }
            ''',
            variables={
                "country_IsoCode2_Iexact": self.countries[4].iso_code_2
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        all_regions = content["data"]["regions"]["edges"]

        self.assertEqual(len(self.regions), len(all_regions))

    def test_fetch_region_by_name(self):
        response = self.query(
            '''
            query region($name: String) {
                region(name: $name) {
                    id
                    name
                    isoCode
                }
            }
            ''',
            variables={
                "name": self.regions[2].name
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        region = content["data"]["region"]

        self.assertEqual(self.regions[2].name, region["name"])

    def test_fetch_region_by_code(self):
        response = self.query(
            '''
            query region($isoCode: String) {
                region(isoCode: $isoCode) {
                    id
                    name
                    isoCode
                }
            }
            ''',
            variables={
                "isoCode": self.regions[3].iso_code
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        region = content["data"]["region"]

        self.assertEqual(self.regions[3].name, region["name"])
