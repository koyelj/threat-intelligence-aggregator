import json
import csv

from pathlib import Path


def load_correlation_results():

    file_path = Path(
        "exports/correlation_results/"
        "correlation_results.json"
    )

    if not file_path.exists():

        raise FileNotFoundError(
            "Correlation results not found. "
            "Run the correlation module first."
        )

    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def generate_blocklists():

    results = load_correlation_results()

    blocklists = {
        "IP": [],
        "DOMAIN": [],
        "URL": [],
        "HASH": [],
        "EMAIL": [],
    }

    for item in results:

        severity = item.get(
            "severity",
            "LOW"
        ).upper()

        if severity not in [
            "HIGH",
            "MEDIUM"
        ]:
            continue

        ioc_type = item.get(
            "type",
            ""
        ).upper()

        value = item.get(
            "ioc"
        )

        if not value:
            continue

        if ioc_type in blocklists:

            blocklists[ioc_type].append(
                value
            )

    return blocklists


def export_txt(blocklists):

    output_directory = Path(
        "exports/blocklists"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    for ioc_type, values in blocklists.items():

        if not values:
            continue

        output_file = (
            output_directory /
            f"{ioc_type.lower()}_blocklist.txt"
        )

        with output_file.open(
            "w",
            encoding="utf-8"
        ) as file:

            for value in values:

                file.write(
                    value + "\n"
                )

        print(
            f"Created: {output_file}"
        )


def export_json(blocklists):

    output_directory = Path(
        "exports/blocklists"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory /
        "blocklists.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            blocklists,
            file,
            indent=4
        )

    print(
        f"Created: {output_file}"
    )


def export_csv(blocklists):

    output_directory = Path(
        "exports/blocklists"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory /
        "blocklists.csv"
    )

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                "IOC",
                "Type"
            ]
        )

        for ioc_type, values in blocklists.items():

            for value in values:

                writer.writerow(
                    [
                        value,
                        ioc_type
                    ]
                )

    print(
        f"Created: {output_file}"
    )


if __name__ == "__main__":

    print("\n================================")
    print("BLOCKLIST GENERATOR")
    print("================================\n")

    blocklists = generate_blocklists()

    for ioc_type, values in blocklists.items():

        print(
            f"{ioc_type}: "
            f"{len(values)} indicators"
        )

    print(
        "\nGenerating blocklists...\n"
    )

    export_txt(blocklists)

    export_json(blocklists)

    export_csv(blocklists)