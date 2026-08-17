from datetime import datetime, timezone

from sqlalchemy import select

from database.connection import engine
from database.models import IOC


def add_ioc(
    value,
    ioc_type,
    source_feed_id=None,
    confidence="Medium",
    severity="Low",
):
    ioc_type = ioc_type.upper()

    now = datetime.now(timezone.utc)
    with engine.begin() as connection:

        result = connection.execute(
            select(IOC).where(
                IOC.value == value,
                IOC.ioc_type == ioc_type,
            )
        )

        existing_ioc = result.first()

        if existing_ioc:

            connection.execute(
                IOC.__table__.update()
                .where(
                    IOC.id == existing_ioc.id
                )
                .values(
                    last_seen=now,
                    occurrence_count=(
                        IOC.occurrence_count + 1
                    ),
                )
            )

            print(
                f"IOC already exists: {value} "
                f"-> updated"
            )

        else:

            new_ioc = {
                "value": value,
                "ioc_type": ioc_type,
                "source_feed_id": source_feed_id,
                "first_seen": now,
                "last_seen": now,
                "confidence": confidence,
                "severity": severity,
                "occurrence_count": 1,
            }

            connection.execute(
                IOC.__table__.insert(),
                new_ioc,
            )

            print(
                f"IOC added: {value} "
                f"-> {ioc_type}"
            )