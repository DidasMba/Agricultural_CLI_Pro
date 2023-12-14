from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)

class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(Integer, primary_key=True)
    course_name = Column(String, nullable=False)
    description = Column(String)
    instructor_id = Column(Integer, ForeignKey('users.user_id'))
    start_date = Column(Date)
    end_date = Column(Date)

class Lesson(Base):
    __tablename__ = 'lessons'
    lesson_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    lesson_title = Column(String, nullable=False)
    content = Column(String)
    video_audio_links = Column(String)

class Assignment(Base):
    __tablename__ = 'assignments'
    assignment_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'))
    instructor_id = Column(Integer, ForeignKey('users.user_id'))
    description = Column(String)
    deadline = Column(Date)

enrollments = Table(
    'user_course_enrollments',
    Base.metadata,
    Column('enrollment_id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('course_id', Integer, ForeignKey('courses.course_id'))
)  

class UserCourseProgress(Base):
    __tablename__ = 'user_course_progress'
    progress_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    course_id = Column(Integer, ForeignKey('courses.course_id'))
