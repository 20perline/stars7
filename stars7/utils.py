from datetime import datetime
from datetime import timedelta
import random
import string


def get_last_draw_day():
    today = datetime.today()
    if today.weekday() in [1, 4, 6] and today.hour > 20:
        return today.strftime('%Y-%m-%d')
    for i in range(1, 7):
        past_date = today - timedelta(days=i)
        wd = past_date.weekday()
        if wd in [1, 4, 6]:
            return past_date.strftime('%Y-%m-%d')


def list_to_str(list1, join_str=" "):
    return join_str.join([str(c) for c in list1])


def list_all_same(list1):
    return all(s == list1[0] for s in list1)


def list_all_even(list1):
    return all(s % 2 == 0 for s in list1)


def list_arithmetical_series(list1):

    def _is_arith_series(list1):
        diff = list1[1] - list1[0]
        n = len(list1)
        for i in range(2, n):
            if list1[i] - list1[i - 1] != diff:
                return False
        return True

    list2 = [x if x != 0 else 10 for x in list1]
    return _is_arith_series(list1) or _is_arith_series(list2)


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


def next_greater_than(a, b):
    for i in range(10):
        a1 = a + i * 10
        if a1 > b:
            return a1


if __name__ == '__main__':
    # day = get_last_draw_day()
    # print(day)
    # a = next_greater_than(9, 6)
    # print(a)
    print(list_arithmetical_series([4, 2, 0, 8]))
    print(list_arithmetical_series([0, 2, 4, 6]))
    print(list_arithmetical_series([0, 8, 6, 4]))
    print(list_arithmetical_series([4, 6, 8, 0]))
    # print(list_in_decrement([6, 5, 3]))
