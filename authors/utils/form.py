from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_value):
    current_value = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{current_value} {attr_new_value}'.strip()


def add_placeholder(field, placeholder):
    add_attr(field, 'placeholder', placeholder)


def check_last_name(last_name):
    if last_name == 'Gantus':
        raise ValidationError(
            ('Last name could not be Gantus'), code='invalid')
