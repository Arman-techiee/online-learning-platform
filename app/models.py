# app/models.py
"""
Database models for LearnHub Online Learning Platform
Includes User, Course, Enrollment, Lesson, Assignment, and LessonProgress models
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


# ============================================================================
# USER MODEL
# ============================================================================

class User(UserMixin, db.Model):
    """User model for students, instructors, and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, instructor, admin
    profile_pic = db.Column(db.String(255), default='default.jpg')
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    courses_teaching = db.relationship('Course', backref='instructor', lazy='dynamic', 
                                      foreign_keys='Course.instructor_id')
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic',
                                 cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


# ============================================================================
# COURSE MODEL
# ============================================================================

class Course(db.Model):
    """Course model for learning content"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, default=0.0)
    difficulty = db.Column(db.String(20), default='Beginner')  # Beginner, Intermediate, Advanced
    image = db.Column(db.String(255), default='default_course.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic', 
                            cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='course', lazy='dynamic', 
                                 cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic', 
                                 cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.title}>'


# ============================================================================
# ENROLLMENT MODEL
# ============================================================================

class Enrollment(db.Model):
    """Enrollment model for student-course relationships"""
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Integer, default=0)  # 0-100 percentage
    completed = db.Column(db.Boolean, default=False)
    
    # Relationships
    lesson_progress = db.relationship('LessonProgress', backref='enrollment', 
                                     lazy='dynamic', cascade='all, delete-orphan')
    
    # Ensure a student can only enroll once per course
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', 
                                          name='unique_enrollment'),)
    
    def __repr__(self):
        return f'<Enrollment Student:{self.student_id} Course:{self.course_id}>'


# ============================================================================
# LESSON MODEL (UPDATED WITH PDF SUPPORT)
# ============================================================================

class Lesson(db.Model):
    """Lesson model for course content"""
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)  # Sequence number
    video_url = db.Column(db.String(255))  # Optional video link
    duration = db.Column(db.Integer)  # Duration in minutes
    pdf_file = db.Column(db.String(255))  # PDF attachment filename - NEW FIELD
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress_records = db.relationship('LessonProgress', backref='lesson', 
                                      lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lesson {self.title}>'


# ============================================================================
# LESSON PROGRESS MODEL (FOR TRACKING)
# ============================================================================

class LessonProgress(db.Model):
    """Track individual lesson completion for students"""
    __tablename__ = 'lesson_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    time_spent = db.Column(db.Integer, default=0)  # Time spent in seconds
    
    # Ensure one progress record per enrollment-lesson pair
    __table_args__ = (db.UniqueConstraint('enrollment_id', 'lesson_id', 
                                          name='unique_lesson_progress'),)
    
    def __repr__(self):
        return f'<LessonProgress Enrollment:{self.enrollment_id} Lesson:{self.lesson_id}>'


# ============================================================================
# ASSIGNMENT MODEL
# ============================================================================

class Assignment(db.Model):
    """Assignment model for course assessments"""
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Assignment {self.title}>'