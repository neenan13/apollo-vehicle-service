import os
from app.database import Base, engine
from app.models import Vehicle

DB_FILE = "vehicles.db"

# Remove old database.

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
    print("Removed existing vehicles.db")

# Recreates empty schema.

Base.metadata.create_all(bind=engine)
print("Created new empty vehicles.db")