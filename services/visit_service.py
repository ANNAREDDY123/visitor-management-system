def valid_phone(phone):

    return (
        phone.isdigit()
        and len(phone) == 10
    )


def valid_visit_time(check_in, check_out):

    return check_out > check_in
