from sqlalchemy import select

from database.connection import engine
from database.models import IOC

from enrichment.enricher import enrich_ioc


def enrich_all_iocs():

    with engine.connect() as connection:

        rows = connection.execute(
            select(IOC)
        ).fetchall()

    enriched = []

    for row in rows:

        result = enrich_ioc(
            value=row.value,
            ioc_type=row.ioc_type,
            occurrence_count=row.occurrence_count,
            confidence=row.confidence,
            severity=row.severity,
        )

        enriched.append(result)

    return enriched


if __name__ == "__main__":

    results = enrich_all_iocs()

    print(
        f"\nEnriched IOCs: {len(results)}"
    )

    for result in results[:10]:
        print(result)