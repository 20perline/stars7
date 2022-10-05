
def list_to_str(list1):
    return ' '.join([str(c) for c in list1])


def coordinates_same_row(list1):
    return all(element.row == list1[0].row for element in list1)