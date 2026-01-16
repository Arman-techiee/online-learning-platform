from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Username must be between 3 and 80 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Please enter a valid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('instructor', 'Instructor')
    ], validators=[DataRequired()])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[
        DataRequired(),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=20, message='Description must be at least 20 characters')
    ])
    category = SelectField('Category', choices=[
        ('Programming', 'Programming'),
        ('Web Development', 'Web Development'),
        ('Data Science', 'Data Science'),
        ('Business', 'Business'),
        ('Design', 'Design'),
        ('Marketing', 'Marketing'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    difficulty = SelectField('Difficulty Level', choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ], validators=[DataRequired()])
    image = FileField('Course Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    is_published = BooleanField('Publish Course')

class LessonForm(FlaskForm):
    title = StringField('Lesson Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    order = IntegerField('Lesson Order', validators=[DataRequired()])
    video_url = StringField('Video URL (Optional)', validators=[Optional(), Length(max=255)])
    duration = IntegerField('Duration (minutes)', validators=[Optional()])
    pdf_file = FileField('PDF Attachment (Optional)', validators=[
        Optional(),
        FileAllowed(['pdf'], 'PDF files only!')
    ])

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    profile_pic = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])