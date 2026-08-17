import csv
import json
from pathlib import Path

from sqlalchemy import func, select

from database.connection import engine
from database.models import IOC, Feed

from correlation.risk_engine import (
    calculate_risk_score,
    calculate_severity,
)


def get_feed_names(ioc_value):

    with engine.connect() as connection:

        query = (
            select(Feed.feed_name)
            .join(
                IOC,
                IOC.source_feed_id == Feed.id
            )
            .where(
                IOC.value == ioc_value
            )
            .distinct()
        )

        result = connection.execute(query)

        return [
            row.feed_name
            for row in result
        ]


def find_cross_feed_iocs():

    with engine.connect() as connection:

        query = (
            select(
                IOC.value,
                IOC.ioc_type,
                func.count(IOC.id).label(
                    "occurrence_count"
                ),
                func.count(
                    func.distinct(
                        IOC.source_feed_id
                    )
                ).label(
                    "feed_count"
                ),
            )
            .join(
                Feed,
                Feed.id == IOC.source_feed_id
            )
            .group_by(
                IOC.value,
                IOC.ioc_type
            )
            .having(
                func.count(
                    func.distinct(
                        IOC.source_feed_id
                    )
                ) > 1
            )
            .order_by(
                func.count(
                    func.distinct(
                        IOC.source_feed_id
                    )
                ).desc()
            )
        )

        result = connection.execute(query)

        return result.fetchall()


def export_csv(correlated_iocs):

    output_directory = Path(
        "exports/correlation_results"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory /
        "correlation_results.csv"
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
                "Type",
                "Occurrence Count",
                "Feed Count",
                "Severity",
                "Risk Score",
                "Sources",
            ]
        )

        for ioc in correlated_iocs:

            severity = calculate_severity(
                ioc.feed_count
            )

            risk_score = calculate_risk_score(
                ioc.feed_count,
                ioc.occurrence_count
            )

            feed_names = get_feed_names(
                ioc.value
            )

            writer.writerow(
                [
                    ioc.value,
                    ioc.ioc_type,
                    ioc.occurrence_count,
                    ioc.feed_count,
                    severity,
                    risk_score,
                    ", ".join(feed_names),
                ]
            )

    print(
        f"CSV report created: {output_file}"
    )


def export_json(correlated_iocs):

    output_directory = Path(
        "exports/correlation_results"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    results = []

    for ioc in correlated_iocs:

        severity = calculate_severity(
            ioc.feed_count
        )

        risk_score = calculate_risk_score(
            ioc.feed_count,
            ioc.occurrence_count
        )

        feed_names = get_feed_names(
            ioc.value
        )

        results.append(
            {
                "ioc": ioc.value,
                "type": ioc.ioc_type,
                "occurrence_count":
                    ioc.occurrence_count,
                "feed_count":
                    ioc.feed_count,
                "severity":
                    severity,
                "risk_score":
                    risk_score,
                "sources":
                    feed_names,
            }
        )

    output_file = (
        output_directory /
        "correlation_results.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            results,
            file,
            indent=4
        )

    print(
        f"JSON report created: {output_file}"
    )


if __name__ == "__main__":

    print("\n================================")
    print("CROSS-FEED CORRELATION")
    print("================================\n")

    correlated_iocs = find_cross_feed_iocs()

    print(
        f"Cross-feed IOCs found: "
        f"{len(correlated_iocs)}"
    )

    export_json(
        correlated_iocs
    )

    export_csv(
        correlated_iocs
    )

    if not correlated_iocs:

        print(
            "No cross-feed IOCs found."
        )

    else:

        for ioc in correlated_iocs:

            severity = calculate_severity(
                ioc.feed_count
            )

            risk_score = calculate_risk_score(
                ioc.feed_count,
                ioc.occurrence_count
            )

            print(
                f"\nIOC: {ioc.value}"
            )

            print(
                f"Type: {ioc.ioc_type}"
            )

            print(
                f"Occurrences: "
                f"{ioc.occurrence_count}"
            )

            print(
                f"Feed Count: "
                f"{ioc.feed_count}"
            )

            print(
                f"Severity: {severity}"
            )

            print(
                f"Risk Score: "
                f"{risk_score}/100"
            )

            print("Sources:")

            feed_names = get_feed_names(
                ioc.value
            )

            for feed_name in feed_names:

                print(
                    f"  - {feed_name}"
                )

            print(
                "----------------------------"
            )