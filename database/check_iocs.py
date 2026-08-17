from database.connection import engine
from database.models import IOC

from sqlalchemy import select


with engine.connect() as connection:

    rows = connection.execute(
        select(IOC)
        .order_by(IOC.id.desc())
        .limit(10)
    ).fetchall()

    print("\nRecent IOCs")
    print("===========")

    for row in rows:
        print(
            row.value,
            "|",
            row.ioc_type,
            "|",
            "Occurrences:",
            row.occurrence_count
        )