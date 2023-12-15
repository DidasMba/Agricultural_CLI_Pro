import sys
from pathlib import Path

# Add the 'database' directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Course, Lesson, Assignment
from datetime import datetime
from cli.courses import courses_cli #import the 'courses_cli'

# Define the engine
engine = create_engine('sqlite:///educational_system.db', echo=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Function to create a session
def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

@click.group()
def cli():
    pass

@cli.command()
def view_lessons():
    """View available lessons."""
    session = create_session()
    lessons = session.query(Lesson).all()
    session.close()

    if not lessons:
        print("No lessons available.")
        return

    for lesson in lessons:
        print(f"Lesson ID: {lesson.lesson_id}, Title: {lesson.lesson_title}")
        # Add more details as needed

@cli.command()
@click.option('--user', prompt='Your username', help='Your username for assignment submission.')
@click.option('--lesson-id', prompt='Lesson ID', type=int, help='ID of the lesson you want to view.')
def view_lesson(user, lesson_id):
    """View a specific lesson."""
    session = create_session()

    # Check if the user exists
    user_obj = session.query(User).filter_by(username=user).first()
    if not user_obj:
        print(f"User '{user}' not found.")
        session.close()
        return

    # Check if the lesson exists
    lesson = session.query(Lesson).get(lesson_id)
    if not lesson:
        print(f"Lesson with ID {lesson_id} not found.")
        session.close()
        return

    # Implement logic for viewing the lesson content
    print(f"Viewing Lesson {lesson_id} - {lesson.lesson_title}")
    print("Lesson Content:")
    print(lesson.content)

    session.close()

@cli.command()
@click.option('--user', prompt='Your username', help='Your username for assignment submission.')
@click.option('--course-id', prompt='Course ID', type=int, help='ID of the course for assignment submission.')
@click.option('--description', prompt='Assignment description', help='Description of the assignment.')
@click.option('--deadline', prompt='Assignment deadline (YYYY-MM-DD)', help='Deadline for assignment submission.')
def submit_assignment(user, course_id, description, deadline):
    """Submit an assignment."""
    session = create_session()

    # Check if the user exists
    user_obj = session.query(User).filter_by(username=user).first()
    if not user_obj:
        print(f"User '{user}' not found.")
        session.close()
        return

    # Check if the course exists
    course = session.query(Course).get(course_id)
    if not course:
        print(f"Course with ID {course_id} not found.")
        session.close()
        return

    # Convert deadline to datetime object
    deadline_obj = datetime.strptime(deadline, '%Y-%m-%d').date()

    # Create a new assignment
    new_assignment = Assignment(
        course_id=course_id,
        instructor_id=course.instructor_id,  # Assuming the instructor is responsible for assignments
        description=description,
        deadline=deadline_obj
    )

    session.add(new_assignment)
    session.commit()

    print("Assignment submitted successfully!")

    session.close()

if __name__ == '__main__':
    cli()