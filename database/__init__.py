from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_session():
    # Set up the database connection
    engine = create_engine('sqlite:///educational_system.db')  # Update with your database connection details
    Session = sessionmaker(bind=engine)
    return Session()
