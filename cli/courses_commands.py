# cli/courses.py
import click
from sqlalchemy.orm import sessionmaker
from database.models import Course
#from main import create_engine
from sqlalchemy import create_engine

# Function to create a session
def create_session():
    Session = sessionmaker(bind=create_engine())
    return Session()

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
        print(f"Course ID: {course.course_id}, Name: {course.course_name}, Instructor: {course.instructor.username}")
        # Add more details as needed
