import re


class InputValidators:

    @staticmethod
    def is_valid_email(text):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, text) is not None

    @staticmethod
    def is_valid_phone_number(text):
        pattern = r'^09\d{9}$'
        return len(text) == 11 and re.match(pattern, text)
