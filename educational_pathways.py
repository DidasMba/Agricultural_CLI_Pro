import sqlite3
import hashlib
import datetime

# Connect to SQLite database
conn = sqlite3.connect('agricultural_education_hub.db')
cursor = conn.cursor()

# ... (Previous table creations)

# Create Educational Pathways table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS educational_pathways (
        pathway_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        course_id INTEGER,
        completed_lessons TEXT, -- Comma-separated list of completed lesson IDs
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (course_id) REFERENCES courses (course_id)
    )
''')

# Commit changes to the database
conn.commit()

# Close the connection
conn.close()

# Reconnect to SQLite database
conn = sqlite3.connect('agricultural_education_hub.db')
cursor = conn.cursor()

def create_course(instructor_id, course_name, description, start_date, end_date):
    cursor.execute('INSERT INTO courses (course_name, description, instructor_id, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
                   (course_name, description, instructor_id, start_date, end_date))
    conn.commit()
    print("Course created successfully.")

def add_lesson(course_id, lesson_title, content, video_link, audio_link):
    cursor.execute('INSERT INTO lessons (course_id, lesson_title, content, video_link, audio_link) VALUES (?, ?, ?, ?, ?)',
                   (course_id, lesson_title, content, video_link, audio_link))
    conn.commit()
    print("Lesson added successfully.")

def enroll_in_course(user_id, course_id):
    cursor.execute('INSERT INTO educational_pathways (user_id, course_id, completed_lessons) VALUES (?, ?, ?)',
                   (user_id, course_id, ''))
    conn.commit()
    print("Enrolled in the course.")

def view_progress(user_id, course_id):
    cursor.execute('SELECT completed_lessons FROM educational_pathways WHERE user_id=? AND course_id=?', (user_id, course_id))
    result = cursor.fetchone()
    if result:
        completed_lessons = result[0].split(',')
        print(f"User has completed the following lessons: {', '.join(completed_lessons)}")
    else:
        print("User has not enrolled in the course.")

# Example usage:

# Create a course
create_course(instructor_id=1, course_name="Introduction to Agriculture", description="Basic concepts in agriculture",
              start_date=datetime.date(2023, 1, 1), end_date=datetime.date(2023, 2, 1))

# Add lessons to the course
add_lesson(course_id=1, lesson_title="Soil Types", content="Understanding different soil types", video_link="video1.mp4", audio_link="audio1.mp3")
add_lesson(course_id=1, lesson_title="Crop Rotation", content="Benefits of crop rotation", video_link="video2.mp4", audio_link="audio2.mp3")

# Enroll a user in the course
enroll_in_course(user_id=2, course_id=1)

# View user's progress in the course
view_progress(user_id=2, course_id=1)

# Close the connection
conn.close()
