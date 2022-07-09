def is_positive(value):
    try:
        float_value = float(value)
        return float_value >= 0
    except ValueError:
        return False
