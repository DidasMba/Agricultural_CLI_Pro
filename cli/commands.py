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
    class Assignment(Base):
    __tablename__ = 'assignments'

    assignment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    description = Column(String, nullable=False)
    deadline = Column(Date, nullable=False)

    # Add a relationship to the User model
    user = relationship('User', back_populates='assignments')

    # Add a relationship to the Course model
    course = relationship('Course', back_populates='assignments')

    # Add this line to the Course model
    Course.assignments = relationship('Assignment', back_populates='course')

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
@click.option('--username', prompt='Username', help='Username for registration.')
@click.option('--password', prompt='Password', hide_input=True, confirmation_prompt=True, help='Password for registration.')
def register_user(username, password):
    """Register a new user."""
    session = create_session()

    # Check if the username is already taken
    if session.query(User).filter_by(username=username).first():
        print(f"Username '{username}' is already taken. Please choose a different username.")
        session.close()
        return

    # Create a new user
    new_user = User(
        username=username,
        password_hash=hash_password(password),
        role='student'  # Set the default role for registration (you can change this as needed)
    )

    session.add(new_user)
    session.commit()

    print(f"User '{username}' registered successfully!")

    session.close()

if __name__ == '__main__':
    cli()