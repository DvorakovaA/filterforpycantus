from django import forms
from django.contrib.staticfiles import finders
from .fields import RepeatableChoiceWithOtherField
import pandas as pd
from functools import lru_cache

@lru_cache(maxsize=None)
def get_field_choices_from_static(file, column):
    """
    Reads a CSV file from the static directory and returns unique choices for a specified column.
    These choices are used in RepeatableChoiceWithOtherField.

    Args:
        file (str): Name of the CSV file (without extension) located in 'filter/static/'.
        column (str): The column name from which to extract unique choices. 
    """
    path = finders.find(f"filter/{file}.csv")
    if not path:
        print(f"Static file filter/{file}.csv not found.")
        return []
    try:
        values = pd.read_csv(path)
        choices = list(set(values[column].dropna()))
        choices.sort()
        return list(zip(choices, choices))
    except Exception as e:
        print(f"Error reading static/filter/{file}.csv: {e}")
        return []
    
OFFICE_CHOICES = get_field_choices_from_static('office', 'name')
GENRE_CHOICES = get_field_choices_from_static('genre', 'name')
FEAST_CHOICES = get_field_choices_from_static('feast', 'name')
DB_CHOICES = get_field_choices_from_static('db', 'shortcut')

SIGLUM_CHOICES = get_field_choices_from_static('sources', 'siglum')
TITLE_CHOICES = get_field_choices_from_static('sources', 'title')
PROVENANCE_CHOICES = get_field_choices_from_static('sources', 'provenance')
CENTURY_CHOICES = get_field_choices_from_static('sources', 'century')
NUMCENT_CHOICES = get_field_choices_from_static('sources', 'num_century')
CURSUS_CHOICES = get_field_choices_from_static('sources', 'cursus')



class FilterForm(forms.Form):
    """
    Form for filtering PyCantus style data (via pycantus library) based on various criteria.

    Atributes:
        name (CharField): Name of the filtration setting.
        genre_incl (RepeatableChoiceWithOtherField): Genre of records to be included.
        genre_excl (RepeatableChoiceWithOtherField): Genre of records to be excluded.
        office_incl (RepeatableChoiceWithOtherField): Office of records to be included.
        office_excl (RepeatableChoiceWithOtherField): Office of records to be excluded.
        feast_incl (RepeatableChoiceWithOtherField): Feast of records to be included.
        feast_excl (RepeatableChoiceWithOtherField): Feast of records to be excluded.
        db_incl (RepeatableChoiceWithOtherField): Source database of records to be included.
        db_excl (RepeatableChoiceWithOtherField): Source database of records to be excluded.
        siglum_incl (RepeatableChoiceWithOtherField): Siglum of source records to be included.
        siglum_excl (RepeatableChoiceWithOtherField): Siglum of source records to be excluded.
        title_incl (RepeatableChoiceWithOtherField): Title of the source to be included.
        title_excl (RepeatableChoiceWithOtherField): Title of the source to be excluded.
        provenance_incl (RepeatableChoiceWithOtherField): Provenance of the source to be included.
        provenance_excl (RepeatableChoiceWithOtherField): Provenance of the source to be excluded.
        century_incl (RepeatableChoiceWithOtherField): Century of the source to be included.
        century_excl (RepeatableChoiceWithOtherField): Century of the source to be excluded.
        num_century_incl (RepeatableChoiceWithOtherField): Numerical century of the source to be included.
        num_century_excl (RepeatableChoiceWithOtherField): Numerical century of the source to be excluded.
        cursus_incl (RepeatableChoiceWithOtherField): Cursus of the source to be included.
        cursus_excl (RepeatableChoiceWithOtherField): Cursus of the source to be excluded.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'filter_for_my_great_experiment_XY'
        }),
        required=True
    )

    # Include values
    genre_incl = RepeatableChoiceWithOtherField(
        label="Genre",
        choices=GENRE_CHOICES,
        required=False
    )

    office_incl = RepeatableChoiceWithOtherField(
        label="Office",
        choices=OFFICE_CHOICES,
        required=False
    )

    feast_incl = RepeatableChoiceWithOtherField(
        label="Feast",
        choices=FEAST_CHOICES,
        required=False
    )

    db_incl = RepeatableChoiceWithOtherField(
        label="Source database of records",
        choices=DB_CHOICES,
        required=False
    )

    siglum_incl = RepeatableChoiceWithOtherField(
        label="Siglum",
        choices=SIGLUM_CHOICES,
        required=False
    )

    title_incl = RepeatableChoiceWithOtherField(
        label="Title of source",
        choices=TITLE_CHOICES,
        required=False
    )

    provenance_incl = RepeatableChoiceWithOtherField(
        label="Provenance of source",
        choices=PROVENANCE_CHOICES,
        required=False
    )

    century_incl = RepeatableChoiceWithOtherField(
        label="Century of source",
        choices=CENTURY_CHOICES,
        required=False
    )

    num_century_incl = RepeatableChoiceWithOtherField(
        label="Numerical century of source",
        choices=NUMCENT_CHOICES,
        required=False
    )

    cursus_incl = RepeatableChoiceWithOtherField(
        label="Cursus of source",
        choices=CURSUS_CHOICES,
        required=False
    )

    # Exclude values
    genre_excl = RepeatableChoiceWithOtherField(
        label="Genre",
        choices=GENRE_CHOICES,
        required=False
    )

    office_excl = RepeatableChoiceWithOtherField(
        label="Office",
        choices=OFFICE_CHOICES,
        required=False
    )

    feast_excl = RepeatableChoiceWithOtherField(
        label="Feast",
        choices=FEAST_CHOICES,
        required=False
    )

    db_excl = RepeatableChoiceWithOtherField(
        label="Source database of records",
        choices=DB_CHOICES,
        required=False
    )

    siglum_excl = RepeatableChoiceWithOtherField(
        label="Siglum",
        choices=SIGLUM_CHOICES,
        required=False
    )

    title_excl = RepeatableChoiceWithOtherField(
        label="Title of source",
        choices=TITLE_CHOICES,
        required=False
    )

    provenance_excl = RepeatableChoiceWithOtherField(
        label="Provenance of source",
        choices=PROVENANCE_CHOICES,
        required=False
    )

    century_excl = RepeatableChoiceWithOtherField(
        label="Century of source",
        choices=CENTURY_CHOICES,
        required=False
    )

    num_century_excl = RepeatableChoiceWithOtherField(
        label="Numerical century of source",
        choices=NUMCENT_CHOICES,
        required=False
    )

    cursus_excl = RepeatableChoiceWithOtherField(
        label="Cursus of source",
        choices=CURSUS_CHOICES,
        required=False
    )