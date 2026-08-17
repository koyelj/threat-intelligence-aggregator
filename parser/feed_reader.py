import csv
import json
from pathlib import Path

from parser.ioc_parser import identify_ioc

def read_text_feed(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Feed file not found: {file_path}"
        )

    indicators = []

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line_number, line in enumerate(
            file,
            start=1
        ):
            value = line.strip()

            if not value:
                continue

            ioc_type = identify_ioc(value)

            indicators.append(
                {
                    "value": value,
                    "type": ioc_type,
                    "line_number": line_number,
                }
            )

    return indicators


def read_csv_feed(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Feed file not found: {file_path}"
        )

    indicators = []

    with file_path.open(
        "r",
        encoding="utf-8",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for line_number, row in enumerate(
            reader,
            start=2
        ):
            value = row.get("indicator")

            if not value:
                continue

            value = value.strip()

            ioc_type = identify_ioc(value)

            indicators.append(
                {
                    "value": value,
                    "type": ioc_type,
                    "line_number": line_number,
                }
            )

    return indicators

def read_json_feed(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Feed file not found: {file_path}"
        )

    indicators = []

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    for line_number, item in enumerate(
        data.get("indicators", []),
        start=1
    ):

        value = item.get("indicator")

        if not value:
            continue

        value = value.strip()

        ioc_type = identify_ioc(value)

        indicators.append(
            {
                "value": value,
                "type": ioc_type,
                "line_number": line_number,
            }
        )

    return indicators