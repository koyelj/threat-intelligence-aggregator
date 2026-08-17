from datetime import datetime, timezone

from database.connection import engine
from database.models import Feed


with engine.begin() as connection:

    connection.execute(
        Feed.__table__.insert(),
        {
            "feed_name": "Local Remote Test Feed",
            "feed_type": "TXT",
            "source_url": "http://localhost:8000/remote_test_feed.txt",
            "status": "active",
            "created_at": datetime.now(timezone.utc),
        },
    )

print("Feed added successfully.")