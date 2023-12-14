import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User, Course, Lesson, Assignment, enrollments
import bcrypt

engine = create_engine('sqlite:///agricultural_education_hub.db')
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

@click.command()
@click.argument('username')
@click.argument('password')
def register(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username=username, password_hash=hashed_password, role="Student")
    session.add(new_user)
    session.commit()
    click.echo(f"User {username} registered successfully.")

@click.command()
@click.argument('course_name')
@click.argument('description')
def create_course(course_name, description):
    new_course = Course(course_name=course_name, description=description)
    session.add(new_course)
    session.commit()
    click.echo(f"Course {course_name} created successfully.")

@click.command()
def list_courses():
    courses = session.query(Course).all()
    click.echo("Available Courses:")
    for course in courses:
        click.echo(f"{course.course_id}: {course.course_name} - {course.description}")

cli.add_command(register)
cli.add_command(create_course)
cli.add_command(list_courses)

if __name__ == '__main__':
    cli()
