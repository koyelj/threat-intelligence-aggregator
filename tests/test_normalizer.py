from normalization.normalizer import remove_duplicates


def test_remove_duplicates():

    indicators = [
        {
            "value": "Malicious-Example.COM",
            "type": "DOMAIN",
            "line_number": 1,
        },
        {
            "value": "malicious-example.com",
            "type": "DOMAIN",
            "line_number": 2,
        },
        {
            "value": "192.0.2.10",
            "type": "IP",
            "line_number": 3,
        },
        {
            "value": "192.0.2.10",
            "type": "IP",
            "line_number": 4,
        },
    ]

    cleaned = remove_duplicates(
        indicators
    )

    assert len(cleaned) == 2


def test_unknown_indicators_are_removed():

    indicators = [
        {
            "value": "this-is-not-a-valid-ioc",
            "type": "UNKNOWN",
            "line_number": 1,
        }
    ]

    cleaned = remove_duplicates(
        indicators
    )

    assert len(cleaned) == 0