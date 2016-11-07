def check_list_element_in_string(s, l):
    for item in l:
        if item in s:
            return True

    return False