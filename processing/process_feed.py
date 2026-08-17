from parser.feed_reader import (
    read_text_feed,
    read_csv_feed,
    read_json_feed,
)

from feeds.url_feed_processor import process_url_feed
from normalization.normalizer import normalize_indicator
from database.ioc_manager import add_ioc
from enrichment.enricher import enrich_ioc


def process_feed(
    file_path,
    source_feed_id
):

    print("\n============================")
    print("Processing Feed")
    print("============================")

    print(f"Feed: {file_path}")
    print(f"Feed ID: {source_feed_id}")

    print("\nReading feed...")

    file_path_lower = file_path.lower()

    if file_path_lower.startswith(
       ("http://", "https://")
):
      indicators = process_url_feed(
        file_path
    )

    elif file_path_lower.endswith(".csv"):
        indicators = read_csv_feed(file_path)

    elif file_path_lower.endswith(".json"):
        indicators = read_json_feed(file_path)

    elif file_path_lower.endswith(".txt"):
        indicators = read_text_feed(file_path)

    else:
        raise ValueError(
        f"Unsupported feed format: {file_path}"
    )
    clean_indicators = []

    for indicator in indicators:

        normalized = normalize_indicator(
            indicator["value"],
            indicator["type"]
        )

        if normalized:

            clean_indicators.append(
                {
                    "value": normalized,
                    "type": indicator["type"]
                }
            )

    print(
        f"Clean indicators: {len(clean_indicators)}"
    )

    print("\nStoring IOCs in database...")
    print("----------------------------")

    for indicator in clean_indicators:

        enrichment_result = enrich_ioc(
            value=indicator["value"],
            ioc_type=indicator["type"],
        )

        add_ioc(
            value=enrichment_result["value"],
            ioc_type=enrichment_result["ioc_type"],
            source_feed_id=source_feed_id,
            confidence=enrichment_result["confidence"],
            severity=enrichment_result["severity"],
        )

    print("\nFeed processing completed.")


if __name__ == "__main__":

    process_feed(
        file_path="http://localhost:8000/remote_test_feed.txt",
        source_feed_id=1,
    )