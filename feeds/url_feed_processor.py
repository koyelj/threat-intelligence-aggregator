from feeds.feed_downloader import download_feed
from parser.ioc_parser import identify_ioc
from database.ioc_manager import add_ioc


def process_url_feed(url):

    content = download_feed(url)

    indicators = []

    for line_number, line in enumerate(
        content.splitlines(),
        start=1
    ):

        value = line.strip()

        if not value:
            continue

        ioc_type = identify_ioc(value)

        if ioc_type == "UNKNOWN":
            continue

        indicators.append(
            {
                "value": value,
                "type": ioc_type,
                "line_number": line_number,
            }
        )

    return indicators


def store_url_feed(
    url,
    source_feed_id=None,
):

    indicators = process_url_feed(url)

    print("\nStoring URL feed IOCs...")
    print("-------------------------")

    for indicator in indicators:

        add_ioc(
            value=indicator["value"],
            ioc_type=indicator["type"],
            source_feed_id=source_feed_id,
        )

    print(
        "\nURL feed processing completed."
    )