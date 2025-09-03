"""
Script to construct a YAML string from form data for filtration settings used in pycantus library.
"""

import yaml

INCLUDE_KEYS = {
    'genre_incl', 'office_incl', 'feast_incl', 'db_incl', 'siglum_incl',
    'title_incl', 'provenance_incl', 'century_incl', 'num_century_incl',
    'cursus_incl'
}
EXCLUDE_KEYS = {
    'genre_excl', 'office_excl', 'feast_excl', 'db_excl', 'siglum_excl',
    'title_excl', 'provenance_excl', 'century_excl', 'num_century_excl',
    'cursus_excl'
}
TRANSLATE_KEY = {
    'genre_incl': 'genre', 'office_incl': 'office', 'feast_incl': 'feast',
    'db_incl': 'db', 'siglum_incl': 'siglum', 'title_incl': 'title',
    'provenance_incl': 'provenance', 'century_incl': 'century',
    'num_century_incl': 'num_century', 'cursus_incl': 'cursus',
    'genre_excl': 'genre', 'office_excl': 'office', 'feast_excl': 'feast',
    'db_excl': 'db', 'siglum_excl': 'siglum', 'title_excl': 'title',
    'provenance_excl': 'provenance', 'century_excl': 'century',
    'num_century_excl': 'num_century', 'cursus_excl': 'cursus'
}

def construct_yaml(form_data : dict):
    """
    Constructs a YAML string from the provided form data.
    Atributes:
        form_data (dict): Dictionary containing the form data.
    Returns:
        tuple: A tuple containing the name of the filter and the YAML string.
    """
    yaml_data = {
        'name': form_data['name'],
        'include_values': {},
        'exclude_values': {},
    }

    for key in form_data:
        if key in INCLUDE_KEYS and form_data[key]:
            yaml_data['include_values'][TRANSLATE_KEY[key]] = form_data[key]
        elif key in EXCLUDE_KEYS and form_data[key]:
            yaml_data['exclude_values'][TRANSLATE_KEY[key]] = form_data[key]

    return form_data['name'], yaml.dump(yaml_data, sort_keys=False, allow_unicode=True)