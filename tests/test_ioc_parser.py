from parser.ioc_parser import identify_ioc


def test_ip_detection():

    assert identify_ioc(
        "192.0.2.10"
    ) == "IP"


def test_domain_detection():

    assert identify_ioc(
        "malicious-example.com"
    ) == "DOMAIN"


def test_url_detection():

    assert identify_ioc(
        "https://malicious-example.com/login"
    ) == "URL"


def test_email_detection():

    assert identify_ioc(
        "test@example.com"
    ) == "EMAIL"


def test_hash_detection():

    assert identify_ioc(
        "d41d8cd98f00b204e9800998ecf8427e"
    ) == "HASH"


def test_unknown_detection():

    assert identify_ioc(
        "this-is-not-an-ioc"
    ) == "UNKNOWN"