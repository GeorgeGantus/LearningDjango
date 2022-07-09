from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from recipes.models import Recipe

from .utils import is_positive


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # with this var we will throw all the errors in one row
        self.form_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'cover')
        widgets = {
            'cover': forms.FileInput(),
            'servings_unit': forms.Select(
                choices=(
                    ('Portions', 'Portions'),
                    ('Pieces', 'Pieces'),
                    ('Slices', 'Slices')

                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutes', 'Minutes'),
                    ('Hours', 'Hours')
                )
            )
        }

    def clean(self):
        super_clean = super().clean()

        if self.form_errors:
            raise ValidationError(self.form_errors)
        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            self.form_errors['title'].append('Must have at least 5 chars')
        return title

    def clean_servings(self):
        servings = self.cleaned_data['servings']

        if not is_positive(servings):
            self.form_errors['servings'].append('Must be a positive number')

        return servings

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data['preparation_time']

        if not is_positive(preparation_time):
            self.form_errors['preparation_time'].append(
                'Must be a positive number')

        return preparation_time
