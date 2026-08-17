from parser.feed_reader import read_text_feed


def test_read_text_feed():

    indicators = read_text_feed(
        "feeds/sample_iocs.txt"
    )

    assert len(indicators) > 0


def test_feed_contains_ip():

    indicators = read_text_feed(
        "feeds/sample_iocs.txt"
    )

    values = [
        indicator["value"]
        for indicator in indicators
    ]

    assert "192.0.2.10" in values


def test_feed_indicator_structure():

    indicators = read_text_feed(
        "feeds/sample_iocs.txt"
    )

    for indicator in indicators:

        assert "value" in indicator
        assert "type" in indicator
        assert "line_number" in indicator