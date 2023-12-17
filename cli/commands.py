# commands.py

import sys
from pathlib import Path

# Add the 'database' directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import click
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from database.models import User, Course, Lesson, Assignment, Submission, user_course_enrollments

Base = declarative_base()

# Define the engine
engine = create_engine('sqlite:///educational_system.db', echo=True)

# Create tables
Base.metadata.create_all(bind=engine)

# Function to create a session
def create_session():
    Session = sessionmaker(bind=engine)
    return Session()

def hash_password(password):
    # Implement a secure password hashing method (e.g., bcrypt)
    # Replace this with an actual implementation
    return password

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
@click.option('--description', prompt='Assignment description', help='Description of the assignment.')
@click.option('--deadline', prompt='Assignment deadline (YYYY-MM-DD)', help='Deadline for assignment submission.')
def submit_assignment(user, description, deadline):
    """Submit an assignment."""
    session = create_session()

    # Check if the user exists
    user_obj = session.query(User).filter_by(username=user).first()
    if not user_obj:
        print(f"User '{user}' not found.")
        session.close()
        return

    # View available courses
    courses = session.query(Course).all()
    if not courses:
        print("No courses available.")
        session.close()
        return

    print("Available Courses:")
    for course in courses:
        print(f"Course ID: {course.course_id}, Name: {course.course_name}")

    # Prompt the user to select a course
    course_id = click.prompt('Enter the Course ID for assignment submission', type=int)

    # Check if the selected course exists
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
        instructor_id=course.instructor_id,
        description=description,
        deadline=deadline_obj
    )

    session.add(new_assignment)
    session.commit()

    print("Assignment submitted successfully!")

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

@cli.command(name='enroll-course')
@click.option('--user', prompt='Your username', help='Your username for course enrollment.')
@click.option('--course-id', prompt='Course ID', type=int, help='ID of the course for enrollment.')
def enroll_course(user, course_id):
    """Enroll in a course."""
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

    # Check if the user is already enrolled in the course
    enrollment = session.query(user_course_enrollments).filter_by(user_id=user_obj.user_id, course_id=course_id).first()
    if enrollment:
        print(f"User '{user}' is already enrolled in the course with ID {course_id}.")
        session.close()
        return

    # Enroll the user in the course
    try:
        new_enrollment = user_course_enrollments.insert().values(user_id=user_obj.user_id, course_id=course_id)
        session.execute(new_enrollment)
        session.commit()
        print(f"User '{user}' enrolled in the course with ID {course_id} successfully!")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

@cli.command(name='view-users')  # Add the 'view-users' command
def view_users():
    """View all users."""
    session = create_session()
    users = session.query(User).all()
    session.close()

    if not users:
        print("No users available.")
        return

    for user in users:
        print(f"User ID: {user.user_id}, Username: {user.username}, Role: {user.role}")
        # Add more details as needed

@cli.command()
def view_courses():
    """View available courses."""
    session = create_session()
    courses = session.query(Course).all()
    session.close()

    if not courses:
        print("No courses available.")
        return

    for course in courses:
        print(f"Course ID: {course.course_id}, Name: {course.course_name}")
        # Add more details as needed

@cli.command()
@click.option('--user', prompt='Your username', help='Your username for assignment submission.')
@click.option('--lesson-id', prompt='Lesson ID', type=int, help='ID of the lesson for assignment submission.')
@click.option('--description', prompt='Assignment description', help='Description of the assignment.')
@click.option('--deadline', prompt='Assignment deadline (YYYY-MM-DD)', help='Deadline for assignment submission.')
def submit_assignment(user, lesson_id, description, deadline):  # Updated argument to lesson_id
    """Submit an assignment."""
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

    # Convert deadline to datetime object
    deadline_obj = datetime.strptime(deadline, '%Y-%m-%d').date()

    # Create a new assignment using lesson_id instead of course_id
    new_assignment = Assignment(
        lesson_id=lesson_id,  # Use lesson_id instead of course_id
        instructor_id=lesson.course.instructor_id,
        description=description,
        deadline=deadline_obj
    )

    session.add(new_assignment)
    session.commit()

    print("Assignment submitted successfully!")

    session.close()

@cli.command(name='insert-lesson')
@click.option('--course-id', prompt='Course ID', type=int, help='ID of the course for the lesson.')
@click.option('--lesson-title', prompt='Lesson Title', help='Title of the lesson.')
@click.option('--content', prompt='Lesson Content', help='Content of the lesson.')
@click.option('--video-audio-links', prompt='Video/Audio Links', help='Links to video/audio resources.')
def insert_lesson(course_id, lesson_title, content, video_audio_links):
    """Insert a new lesson."""
    session = create_session()

    # Check if the course exists
    course = session.query(Course).get(course_id)
    if not course:
        print(f"Course with ID {course_id} not found.")
        session.close()
        return

    new_lesson = Lesson(
        course_id=course_id,
        lesson_title=lesson_title,
        content=content,
        video_audio_links=video_audio_links
    )

    session.add(new_lesson)
    session.commit()
    print(f"Lesson added successfully: {new_lesson}")

    session.close()

# ... (other commands)

# Keep the rest of the existing code unchanged

if __name__ == '__main__':
    cli()