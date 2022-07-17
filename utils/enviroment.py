import os


def get_env_variable(variable_name, default_value=''):
    return os.environ.get(variable_name, default_value)


def parse_comma_sep_value(comma_sep_value):
    if not comma_sep_value or not isinstance(comma_sep_value, str):
        return []
    return [string.strip() for string in comma_sep_value.split(',') if string]
