import unittest
import yaml

from filter.construct_file import construct_yaml


class ConstructYamlTests(unittest.TestCase):
    def test_construct_yaml_maps_keys_and_omits_empty_lists(self):
        form_data = {
            "name": "example_filter",
            "genre_incl": ["A", "R"],
            "office_incl": [],
            "db_incl": ["CD"],
            "title_incl": [],
            "provenance_incl": [],
            "century_incl": ["12th century"],
            "num_century_incl": ["12"],
            "cursus_incl": [],
            "feast_incl": [],
            "siglum_incl": [],
            "genre_excl": ["H"],
            "office_excl": [],
            "db_excl": [],
            "title_excl": [],
            "provenance_excl": [],
            "century_excl": [],
            "num_century_excl": [],
            "cursus_excl": [],
            "feast_excl": [],
            "siglum_excl": [],
        }

        name, yaml_content = construct_yaml(form_data)

        self.assertEqual(name, "example_filter")
        parsed = yaml.safe_load(yaml_content)
        self.assertEqual(
            parsed,
            {
                "name": "example_filter",
                "include_values": {
                    "genre": ["A", "R"],
                    "db": ["CD"],
                    "century": ["12th century"],
                    "num_century": ["12"],
                },
                "exclude_values": {
                    "genre": ["H"],
                },
            },
        )


if __name__ == "__main__":
    unittest.main()
