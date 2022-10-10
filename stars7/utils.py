import random
import string


def list_to_str(list1):
    return ' '.join([str(c) for c in list1])


def list_all_same(list1):
    return all(s == list1[0] for s in list1)


def list_all_even(list1):
    return all(s % 2 == 0 for s in list1)


def list_all_odd(list1):
    return all(s % 2 != 0 for s in list1)


def list_in_decrement(list1):
    list2 = [v+i for i, v in enumerate(list1)]
    return list_all_same(list2)


def list_in_increment(list1):
    length = len(list1)
    list2 = [v + (length - i) for i, v in enumerate(list1)]
    return list_all_same(list2)


def coordinates_same_row(list1):
    return all(element.row == list1[0].row for element in list1)


def random_str(len):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(len))
