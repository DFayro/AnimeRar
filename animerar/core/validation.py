import re

PASSWORD_FORMAT = "[A-Za-z0-9!?@#$%^&+=]{10,64}"
EMAIL_REGEX_FORMAT = "^[a-zA-Z0-9]+[\._-]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$"


def is_password(str):
    if (re.search(PASSWORD_FORMAT, str)):
        return True
    else:
        return False


def is_email(str):
    if (re.search(EMAIL_REGEX_FORMAT, str)):
        return True
    else:
        return False