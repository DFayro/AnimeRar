import re

PASSWORD_FORMAT = "^[A-Za-z0-9!?@#$%^&+=]{10,64}$"
EMAIL_REGEX_FORMAT = "^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,3})$"


# Private API
def _is_format(str, format):
	if (re.match(format, str)):
		return True

	return False


def is_password(str):
	return _is_format(str, PASSWORD_FORMAT)


def is_email(str):
	return _is_format(str, EMAIL_REGEX_FORMAT)
