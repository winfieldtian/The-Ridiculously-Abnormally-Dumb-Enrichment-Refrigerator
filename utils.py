"""this is a utils file for misc functinos"""

def convert_string_to_cents(dollar_string):
    """Converts a string to an int including the decimal (cents)
    i.e 32.52 converts to 3252, 16.3 converts to 1630
    """

    value = 0
    cents = False
    truncate = 0
    for letter in dollar_string:
        if letter == '.':
            cents = True
            continue
        value *= 10
        value += int(letter)
        if cents is True:
            truncate += 1
            if truncate == 2:
                break

    if cents is False:
        return value * 100
    if truncate == 1:
        return value * 10
    return value

def compute_broker_fee(amount, price):
    max_fee = amount * price / 200
    fee = (3 * amount) / 4
    if fee < 100:
        return 100
    if fee > max_fee:
        return max_fee
    return fee
