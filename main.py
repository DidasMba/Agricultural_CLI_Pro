# main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base

# Connect to the database
engine = create_engine('sqlite:///educational_system.db', echo=True)  # Change the database URL as needed

# Create tables
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Close the session when done (optional)
# session.close()
