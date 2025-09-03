from django import forms
from .widgets import RepeatableChoiceWithOtherWidget

class RepeatableChoiceWithOtherField(forms.Field):
    """
    A field that uses RepeatableChoiceWithOtherWidget to allow users to select from a list of choices
    or add custom options.
    """
    def __init__(self, choices=[], *args, **kwargs):
        self.choices = choices
        kwargs['widget'] = RepeatableChoiceWithOtherWidget(choices=choices)
        super().__init__(*args, **kwargs)

    def clean(self, value):
        return value