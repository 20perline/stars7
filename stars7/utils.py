import random
import string


def list_to_str(list1):
    return ' '.join([str(c) for c in list1])


def coordinates_same_row(list1):
    return all(element.row == list1[0].row for element in list1)


def random_str(len):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))
