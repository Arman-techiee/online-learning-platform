"""
Database initialization script
Run this file to create the database and add sample data
"""

from app import create_app, db
from app.models import User, Course, Lesson, Assignment
from datetime import datetime, timedelta

def init_database():
    """Initialize the database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate (WARNING: This deletes all data!)
        print("Creating database tables...")
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@learnhub.com',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create sample instructor
        print("Creating instructor...")
        instructor = User(
            username='john_doe',
            email='john@learnhub.com',
            role='instructor',
            bio='Experienced web developer with 10 years of experience'
        )
        instructor.set_password('instructor123')
        db.session.add(instructor)
        
        # Create sample student
        print("Creating student...")
        student = User(
            username='jane_smith',
            email='jane@learnhub.com',
            role='student',
            bio='Enthusiastic learner passionate about technology'
        )
        student.set_password('student123')
        db.session.add(student)
        
        # Commit users first
        db.session.commit()
        
        # Create sample courses
        print("Creating sample courses...")
        
        course1 = Course(
            title='Introduction to Web Development',
            description='Learn the fundamentals of web development including HTML, CSS, and JavaScript. Perfect for beginners who want to start their journey in web development.',
            instructor_id=instructor.id,
            category='Web Development',
            price=49.99,
            difficulty='Beginner',
            is_published=True
        )
        
        course2 = Course(
            title='Advanced Python Programming',
            description='Master advanced Python concepts including decorators, generators, context managers, and more. Ideal for developers looking to level up their Python skills.',
            instructor_id=instructor.id,
            category='Programming',
            price=79.99,
            difficulty='Advanced',
            is_published=True
        )
        
        course3 = Course(
            title='Data Science with Python',
            description='Learn data analysis, visualization, and machine learning using Python. Includes pandas, matplotlib, and scikit-learn.',
            instructor_id=instructor.id,
            category='Data Science',
            price=99.99,
            difficulty='Intermediate',
            is_published=True
        )
        
        db.session.add_all([course1, course2, course3])
        db.session.commit()
        
        # Create sample lessons for course 1
        print("Creating sample lessons...")
        
        lessons_course1 = [
            Lesson(
                course_id=course1.id,
                title='Introduction to HTML',
                content='Learn the basics of HTML including tags, elements, and document structure.',
                order=1,
                duration=30
            ),
            Lesson(
                course_id=course1.id,
                title='CSS Fundamentals',
                content='Understand how to style web pages using CSS including selectors, properties, and the box model.',
                order=2,
                duration=45
            ),
            Lesson(
                course_id=course1.id,
                title='JavaScript Basics',
                content='Introduction to JavaScript programming including variables, functions, and DOM manipulation.',
                order=3,
                duration=60
            )
        ]
        
        db.session.add_all(lessons_course1)
        
        # Create sample assignments
        print("Creating sample assignments...")
        
        assignment1 = Assignment(
            course_id=course1.id,
            title='Build a Personal Portfolio',
            description='Create a personal portfolio website using HTML, CSS, and JavaScript',
            due_date=datetime.utcnow() + timedelta(days=7)
        )
        
        db.session.add(assignment1)
        db.session.commit()
        
        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print("\nDefault login credentials:")
        print("\nAdmin:")
        print("  Email: admin@learnhub.com")
        print("  Password: admin123")
        print("\nInstructor:")
        print("  Email: john@learnhub.com")
        print("  Password: instructor123")
        print("\nStudent:")
        print("  Email: jane@learnhub.com")
        print("  Password: student123")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_database()
