from flask import Flask, render_template

from config import UPLOAD_FOLDER

from database.connection import engine
from database.models import Feed, IOC

from sqlalchemy import func, select


app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():

    with engine.connect() as connection:

        feed_count = connection.execute(
            select(func.count(Feed.id))
        ).scalar()

        ioc_count = connection.execute(
            select(func.count(IOC.id))
        ).scalar()

        high_severity = connection.execute(
            select(func.count(IOC.id)).where(
                IOC.severity == "High"
            )
        ).scalar()

        feeds = connection.execute(
            select(Feed).order_by(
                Feed.id.desc()
            )
        ).fetchall()

        iocs = connection.execute(
            select(IOC)
            .order_by(IOC.id.desc())
            .limit(10)
        ).fetchall()

    return render_template(
        "dashboard.html",
        feed_count=feed_count,
        ioc_count=ioc_count,
        high_severity=high_severity,
        feeds=feeds,
        iocs=iocs,
    )


if __name__ == "__main__":
    app.run(debug=True)