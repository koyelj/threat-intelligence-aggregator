import ipaddress
import re


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)


HASH_PATTERN = re.compile(
    r"^[a-fA-F0-9]+$"
)


def is_ip(value):
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def is_email(value):
    return bool(EMAIL_PATTERN.match(value))


def is_hash(value):
    if len(value) not in (32, 40, 64):
        return False

    return bool(HASH_PATTERN.match(value))


def is_url(value):
    return value.startswith(
        ("http://", "https://")
    )


def is_domain(value):
    pattern = (
        r"^(?=.{1,253}$)"
        r"(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}"
        r"[a-zA-Z0-9])?\.)+"
        r"[a-zA-Z]{2,}$"
    )

    return bool(re.match(pattern, value))


def identify_ioc(value):
    value = value.strip()

    if not value:
        return None

    if is_ip(value):
        return "IP"

    if is_url(value):
        return "URL"

    if is_email(value):
        return "EMAIL"

    if is_hash(value):
        return "HASH"

    if is_domain(value):
        return "DOMAIN"

    return "UNKNOWN"