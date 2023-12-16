# cli/courses.py
import click
from sqlalchemy.orm import Session
from database.models import Course
from database import get_session



# cli/courses.py
#import click
#from sqlalchemy.orm import sessionmaker
#from database.models import Course
#from main import create_engine
#from sqlalchemy import create_engine

# Importez la classe de modèle Course
# Ajoutez cette ligne au début de courses_commands.py
# Modifiez cette ligne au début de courses_commands.py

from sqlalchemy.orm import Session
from database import get_session  # Importez la fonction get_session


# Function to create a session
def create_session():
    #Session = sessionmaker(bind=create_engine('sqlite:///educational_system.db', echo=True))
    #return Session()
    return create_engine('sqlite:///educational_system.db')

@click.group()
def courses_cli():
    pass

@courses_cli.command()
def view_courses():
    """View available courses."""
    # Use the get_session function to obtain a session
    session = get_session()

    try:
        courses = session.query(Course).all()
        
        print("Courses:")
        for course in courses:
            print(f"Course ID: {course.course_id}, Course Name: {course.course_name}")
            # Add more details as needed

    finally:
        # Close the session to release resources
        session.close()

# If this script is run directly, invoke the CLI
if __name__ == '__main__':
    courses_cli()
