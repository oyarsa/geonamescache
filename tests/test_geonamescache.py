# -*- coding: utf-8 -*-
import unittest
from geonamescache import GeonamesCache


class GeonamesCacheTestSuite(unittest.TestCase):
    """GeonamesCache test cases."""

    def setUp(self):
        self.geonamescache = GeonamesCache()

    def test_continents(self):
        continents = self.geonamescache.get_continents()
        testdata = (
            ('AF', 'Africa'),
            ('AN', 'Antarctica'),
            ('AS', 'Asia'),
            ('EU', 'Europe'),
            ('NA', 'North America'),
            ('OC', 'Oceania'),
            ('SA', 'South America')
        )
        for code, name in testdata:
            self.assertTrue(code in continents)
            self.assertEqual(name, continents[code]['name'])

        for code in ['XX', 'OO']:
            self.assertTrue(code not in continents)

    def test_get_countries(self):
        countries = self.geonamescache.get_countries()

        testdata = (('ES', 'Spain'), ('FR', 'France'), ('US', 'United States'))
        for code, name in testdata:
            self.assertTrue(code in countries)
            self.assertEqual(name, countries[code]['name'])

        for code in ['XX', 'OO']:
            self.assertTrue(code not in countries)

    def test_us_states(self):
        us_states = self.geonamescache.get_us_states()

        testdata = (
            ('NM', 'New Mexico'), ('CA', 'California'), ('NV', 'Nevada'))
        for code, name in testdata:
            self.assertTrue(code in us_states)
            self.assertEqual(name, us_states[code]['name'])

        for code in ['XX', 'OO']:
            self.assertTrue(code not in us_states)

    def test_get_countries_by_names(self):
        # Length of get_countries_by_names dict and get_countries dict must be
        # the same, unless country names wouldn't be unique.
        self.assertTrue(len(self.geonamescache.get_countries_by_names()),
                        len(self.geonamescache.get_countries()))

    def test_get_cities_by_name(self):
        cities = self.geonamescache.get_cities()
        for gid, name in (('3191316', 'Samobor'), ('3107112', 'Rivas-Vaciamadrid')):
            self.assertEqual(name, cities[gid]['name'])

    def test_get_cities_by_name_madrid(self):
        self.assertEqual(
            2, len(self.geonamescache.get_cities_by_name('Madrid')))

    def test_cities_in_us_states(self):
        cities = self.geonamescache.get_cities()
        for gid, name, us_state in (('4164138', 'Miami', 'FL'), ('4525353', 'Springfield', 'OH')):
            self.assertEqual(name, cities[gid]['name'])
            self.assertEqual(us_state, cities[gid]['admin1code'])

    def test_search_cities_case_insensitive(self):
        city_names = ['Kiev', 'kiev']
        for name in city_names:
            cities = self.geonamescache.search_cities(name, case=False)
            self.assertGreaterEqual(len(cities), 1)

    def test_search_cities_case_default(self):
        city_names = ['Kiev', 'kiev']
        expected = [1, 0]
        for name, value in zip(city_names, expected):
            cities = self.geonamescache.search_cities(name)
            self.assertGreaterEqual(len(cities), value)

    def test_us_counties_len(self):
        # Make sure there are 3235 counties, which includes Puerto Rico etc.
        us_counties = self.geonamescache.get_us_counties()
        self.assertEqual(3234, len(us_counties))


if __name__ == '__main__':
    unittest.main()
