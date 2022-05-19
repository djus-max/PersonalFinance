import re


def division_of_amount(value):
    result = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1 ", "%d" % value)
    return result
