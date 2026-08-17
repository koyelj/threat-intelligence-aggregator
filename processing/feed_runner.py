from datetime import datetime, timezone

from sqlalchemy import select

from database.connection import engine
from database.models import Feed

from processing.process_feed import process_feed


def get_active_feeds():

    with engine.connect() as connection:

        result = connection.execute(
            select(Feed).where(
                Feed.status == "active"
            )
        )

        return result.fetchall()


def run_all_feeds():

    feeds = get_active_feeds()

    print("\n============================")
    print("ACTIVE FEEDS")
    print("============================")

    print(
        f"Total active feeds: {len(feeds)}"
    )

    successful = 0
    failed = 0

    for feed in feeds:

        print("\n----------------------------")
        print(f"Feed ID: {feed.id}")
        print(f"Feed Name: {feed.feed_name}")
        print(f"Feed Type: {feed.feed_type}")
        print(f"Source: {feed.source_url}")

        try:

            process_feed(
                file_path=feed.source_url,
                source_feed_id=feed.id,
            )

            with engine.begin() as connection:

                connection.execute(
                    Feed.__table__.update()
                    .where(
                        Feed.id == feed.id
                    )
                    .values(
                        last_updated=
                        datetime.now(timezone.utc)
                    )
                )

            successful += 1

        except Exception as error:

            failed += 1

            print(
                f"\nFeed processing failed: {error}"
            )

            print(
                "Skipping this feed..."
            )

    print("\n============================")
    print("FEED RUN SUMMARY")
    print("============================")

    print(
        f"Successful feeds: {successful}"
    )

    print(
        f"Failed feeds: {failed}"
    )


if __name__ == "__main__":

    run_all_feeds()