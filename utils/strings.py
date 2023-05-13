def is_positive_number(value):
    try:
        num_string = float(value)

    except ValueError:
        return False

    return num_string > 0
