# processCharacter

import re


def get_valid_chars(input_str):
    valid_chars = ""
    for char in input_str:
        if char.isalnum() or char in ['-', '.']:
            valid_chars += char
    return valid_chars

