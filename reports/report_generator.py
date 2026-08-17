from correlation.risk_engine import calculate_severity

import json
from pathlib import Path

from sqlalchemy import select, func

from database.connection import engine
from database.models import Feed, IOC

from datetime import datetime, timezone


def get_severity_counts():

    with engine.connect() as connection:

        result = connection.execute(
            select(
                IOC.value,
                func.count(
                    func.distinct(
                        IOC.source_feed_id
                    )
                ).label(
                    "feed_count"
                )
            )
            .group_by(
                IOC.value
            )
        )

        severity_counts = {
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for row in result:

            severity = calculate_severity(
                row.feed_count
            )

            severity_counts[
                severity
            ] += 1

        return severity_counts

def get_feed_count():

    with engine.connect() as connection:

        result = connection.execute(
            select(
                func.count(Feed.id)
            )
        )

        return result.scalar_one()


def get_total_ioc_count():

    with engine.connect() as connection:

        result = connection.execute(
            select(
                func.count(IOC.id)
            )
        )

        return result.scalar_one()


def get_unique_ioc_count():

    with engine.connect() as connection:

        result = connection.execute(
            select(
                func.count(
                    func.distinct(IOC.value)
                )
            )
        )

        return result.scalar_one()


def get_ioc_type_counts():

    with engine.connect() as connection:

        result = connection.execute(
            select(
                IOC.ioc_type,
                func.count(IOC.id)
            )
            .group_by(
                IOC.ioc_type
            )
        )

        return {
            row[0]: row[1]
            for row in result
        }


def generate_report():

    severity_counts = get_severity_counts()

    report = {
        "summary": {
            "feeds_processed":
                get_feed_count(),

            "total_iocs":
                get_total_ioc_count(),

            "unique_iocs":
                get_unique_ioc_count(),
        },

        "ioc_types":
            get_ioc_type_counts(),

        "severity":
            severity_counts,
    }

    return report

def export_report_json(report):

    output_directory = Path(
        "exports/reports"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory /
        "threat_report.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print(
        f"\nReport created: "
        f"{output_file}"
    )
    
def export_report_txt(report):

    output_directory = Path(
        "exports/reports"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file = (
        output_directory /
        "threat_report.txt"
    )

    summary = report["summary"]
    ioc_types = report["ioc_types"]
    severity = report["severity"]

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "========================================\n"
        )

        file.write(
            "       THREAT INTELLIGENCE REPORT\n"
        )

        file.write(
            "========================================\n\n"
        )

        file.write(
            "Generated: "
            f"{datetime.now(timezone.utc)}\n\n"
        )

        file.write(
            "SUMMARY\n"
        )

        file.write(
            "----------------------------------------\n"
        )

        file.write(
            f"Feeds Processed : "
            f"{summary['feeds_processed']}\n"
        )

        file.write(
            f"Total IOCs      : "
            f"{summary['total_iocs']}\n"
        )

        file.write(
            f"Unique IOCs     : "
            f"{summary['unique_iocs']}\n\n"
        )

        file.write(
            "IOC TYPES\n"
        )

        file.write(
            "----------------------------------------\n"
        )

        for ioc_type, count in ioc_types.items():

            file.write(
                f"{ioc_type:<15}: {count}\n"
            )

        file.write("\n")

        file.write(
            "SEVERITY\n"
        )

        file.write(
            "----------------------------------------\n"
        )

        for level, count in severity.items():

            file.write(
                f"{level:<15}: {count}\n"
            )

        file.write("\n")

        file.write(
            "========================================\n"
        )

        file.write(
            "End of Threat Intelligence Report\n"
        )

        file.write(
            "========================================\n"
        )

    print(
        f"Text report created: "
        f"{output_file}"
    )   

if __name__ == "__main__":

    print("\n================================")
    print("THREAT INTELLIGENCE REPORT")
    print("================================\n")

    print(
        "Feeds:",
        get_feed_count()
    )

    print(
        "Total IOCs:",
        get_total_ioc_count()
    )

    print(
        "Unique IOCs:",
        get_unique_ioc_count()
    )

    print("\nIOC Types:")

    type_counts = get_ioc_type_counts()
    
    print("\nSeverity:")

severity_counts = get_severity_counts()

for severity, count in severity_counts.items():

    print(
        f"{severity}: {count}"
    )

    for ioc_type, count in type_counts.items():

        print(
            f"{ioc_type}: {count}"
        )
        
        report = generate_report()

export_report_json(
    report
)

export_report_txt(
    report
)