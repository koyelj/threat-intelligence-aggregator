from database.connection import engine
from sqlalchemy import text


query = text("""
    SELECT
        value,
        ioc_type,
        occurrence_count
    FROM iocs
    WHERE value IN (
        '192.0.2.210',
        '198.51.100.210',
        'remote-malicious-example.com',
        'attacker-remote@example.com'
    )
    ORDER BY id
""")


with engine.connect() as connection:

    rows = connection.execute(query)

    for row in rows:

        print(row)