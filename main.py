# main.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Course, UserCourseProgress
from datetime import datetime
from cli.courses_commands import view_courses as courses_cli
from cli import cli
from sqlalchemy.orm import Session
from user_manager import UserManager


cli.add_command(courses_cli)  # Add the 'courses_cli'



# Connect to the database
engine = create_engine('sqlite:///educational_system.db', echo=True)  # Change the database URL as needed

# Create tables
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Query and print all users
def query_users(session):
    users = session.query(User).all()
    for user in users:
        print(f"User ID: {user.user_id}, Username: {user.username}, Role: {user.role}")

# Insert a new user
def insert_user(session, username, password_hash, role):
    # Check if the username already exists
    existing_user = session.query(User).filter_by(username=username).first()
    
    if existing_user:
        # If it exists, generate a new unique username
        username = generate_unique_username(session, username)
    
    new_user = User(username=username, password_hash=password_hash, role=role)
    session.add(new_user)
    session.commit()
    print("User added successfully!")

def generate_unique_username(session, username):
    # Generate a new unique username by appending a number
    suffix = 1
    new_username = f"{username}_{suffix}"
    
    # Check if the newly generated username already exists
    while session.query(User).filter_by(username=new_username).first():
        suffix += 1
        new_username = f"{username}_{suffix}"

    return new_username

# Query and print all courses
def query_courses(session):
    courses = session.query(Course).all()
    for course in courses:
        print(f"Course ID: {course.course_id}, Course Name: {course.course_name}")

# Insert a new course
def insert_course(session, course_name, description, instructor_id, start_date, end_date):
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

    new_course = Course(
        course_name=course_name,
        description=description,
        instructor_id=instructor_id,
        start_date=start_date_obj,
        end_date=end_date_obj
    )

    session.add(new_course)
    session.commit()
    print("Course added successfully!")

# Add this line to the existing code
Base.metadata.create_all(bind=engine)

# Examples
query_users(session)
insert_user(session, 'daniel_moan', 'hashed_password', 'student')

query_courses(session)
insert_course(session, 'Introduction to Python', 'Learn Python programming basics', 1, '2023-01-01', '2023-02-01')

# Close the session when done (optional)
session.close()



if __name__ == '__main__':
    
    cli()