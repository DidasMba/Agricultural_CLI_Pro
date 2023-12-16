# cli/courses.py
import click
from sqlalchemy.orm import sessionmaker
from database.models import Course
#from main import create_engine
from sqlalchemy import create_engine

# Importez la classe de modèle Course
# Ajoutez cette ligne au début de courses_commands.py
# Modifiez cette ligne au début de courses_commands.py
from database.models import Course



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
    session = create_session()
    courses = session.query(Course).all()
    session.close()

    if not courses:
        print("No courses available.")
        return

    for course in courses:
         print(f"Course ID: {course.course_id}, Course Name: {course.course_name}")
        # Add more details as needed
