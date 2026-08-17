from database.connection import engine
from sqlalchemy import text


with engine.connect() as connection:

    rows = connection.execute(
        text(
            "SELECT id, feed_name, status, last_updated "
            "FROM feeds "
            "ORDER BY id DESC "
            "LIMIT 5"
        )
    ).fetchall()

    for row in rows:
        print(row)