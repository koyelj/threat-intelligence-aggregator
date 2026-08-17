from datetime import datetime, timezone

from sqlalchemy import select

from database.connection import engine
from database.models import Feed


def add_feed(
    feed_name,
    feed_type,
    source_url=None,
):
    with engine.connect() as connection:

        existing_feed = connection.execute(
            select(Feed).where(
                Feed.feed_name == feed_name
            )
        ).first()

        if existing_feed:
            print(
                f"Feed '{feed_name}' already exists "
                f"with ID {existing_feed.id}."
            )
            return existing_feed.id

    new_feed = Feed(
        feed_name=feed_name,
        feed_type=feed_type,
        source_url=source_url,
        status="active",
        created_at=datetime.now(timezone.utc),
    )

    with engine.begin() as connection:

        result = connection.execute(
            Feed.__table__.insert().returning(
                Feed.id
            ),
            {
                "feed_name": new_feed.feed_name,
                "feed_type": new_feed.feed_type,
                "source_url": new_feed.source_url,
                "status": new_feed.status,
                "last_updated": new_feed.last_updated,
                "created_at": new_feed.created_at,
            },
        )

        feed_id = result.scalar_one()

    print(
        f"Feed '{feed_name}' added successfully "
        f"with ID {feed_id}."
    )

    return feed_id


def get_all_feeds():

    with engine.connect() as connection:

        result = connection.execute(
            select(Feed)
        )

        return result.fetchall()


if __name__ == "__main__":

    add_feed(
        feed_name="Sample OSINT Feed",
        feed_type="TXT",
        source_url="feeds/sample_iocs.txt",
    )

    add_feed(
        feed_name="Secondary OSINT Feed",
        feed_type="TXT",
        source_url="feeds/feed2_iocs.txt",
    )

    add_feed(
        feed_name="Community Threat Feed",
        feed_type="TXT",
        source_url="feeds/feed3_iocs.txt",
    )

    print("\nAvailable Feeds:\n")

    feeds = get_all_feeds()

    for feed in feeds:
        print(feed)