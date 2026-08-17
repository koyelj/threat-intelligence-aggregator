from database.connection import engine
from database.models import Base

print("Creating database tables...")

Base.metadata.create_all(engine)

print("Database tables created successfully!")