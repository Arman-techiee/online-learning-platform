# LearnHub - Online Learning Platform

A full-stack web application for online learning built with Flask, SQLAlchemy, and Bootstrap.

## Features

### User Roles

- **Students**: Browse and enroll in courses, track progress
- **Instructors**: Create and manage courses, add lessons and assignments
- **Admins**: Manage users, courses, and platform content

### Core Functionality

- User authentication and authorization
- Course CRUD operations
- Enrollment system
- Progress tracking
- Search and filter courses
- Responsive design
- Admin dashboard

## Technology Stack

- **Backend**: Python Flask 2.3+
- **Database**: SQLite with Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: jQuery
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. Clone the repository

```bash
git clone <your-repo-url>
cd online-learning-platform
```

2. Create and activate virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Initialize the database

```bash
python init_db.py
```

5. Run the application

```bash
python run.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Default Login Credentials

### Admin

- Email: admin@learnhub.com
- Password: admin123

### Instructor

- Email: john@learnhub.com
- Password: instructor123

### Student

- Email: jane@learnhub.com
- Password: student123

## Project Structure

```
online-learning-platform/
│
├── app/
│   ├── __init__.py           # Application factory
│   ├── models.py             # Database models
│   ├── forms.py              # WTForms
│   ├── auth/                 # Authentication routes
│   ├── main/                 # Main routes
│   ├── courses/              # Course management routes
│   ├── admin/                # Admin panel routes
│   ├── static/               # Static files (CSS, JS, images)
│   └── templates/            # Jinja2 templates
│
├── instance/                 # Instance folder (database)
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── run.py                    # Application entry point
├── init_db.py               # Database initialization
└── README.md                # This file
```

## Features Implementation

### User Authentication

- Registration with role selection
- Secure password hashing
- Login/logout functionality
- Session management

### Course Management

- Create, read, update, delete courses
- Add lessons and assignments
- Course categorization and difficulty levels
- Image upload for courses

### Student Features

- Browse and search courses
- Enroll in courses
- Track learning progress
- View enrolled courses

### Instructor Features

- Create and manage courses
- Add/edit lessons
- View enrolled students
- Publish/unpublish courses

### Admin Features

- User management
- Course management
- Platform statistics
- Delete users and courses

## Database Schema

### Users Table

- id, username, email, password_hash
- role (student/instructor/admin)
- profile_pic, bio, created_at

### Courses Table

- id, title, description
- instructor_id (foreign key)
- category, price, difficulty
- image, created_at, is_published

### Enrollments Table

- id, student_id, course_id
- enrolled_at, progress, completed

### Lessons Table

- id, course_id, title, content
- order, video_url, duration

### Assignments Table

- id, course_id, title, description, due_date

## API Routes

### Authentication

- GET/POST `/auth/register` - User registration
- GET/POST `/auth/login` - User login
- GET `/auth/logout` - User logout

### Main Routes

- GET `/` - Homepage
- GET `/student/dashboard` - Student dashboard
- GET `/instructor/dashboard` - Instructor dashboard
- GET/POST `/profile` - User profile

### Course Routes

- GET `/courses/browse` - Browse courses
- GET `/courses/<id>` - Course details
- POST `/courses/<id>/enroll` - Enroll in course
- GET/POST `/courses/create` - Create course
- GET/POST `/courses/<id>/edit` - Edit course
- POST `/courses/<id>/delete` - Delete course

### Admin Routes

- GET `/admin/dashboard` - Admin dashboard
- GET `/admin/users` - Manage users
- GET `/admin/courses` - Manage courses
- POST `/admin/users/<id>/delete` - Delete user

## Testing

### Manual Testing Checklist

- [ ] User registration and login
- [ ] Create and publish a course
- [ ] Enroll in a course
- [ ] Edit profile
- [ ] Admin user management
- [ ] Search and filter courses
- [ ] Responsive design on mobile

## Deployment

### PythonAnywhere Deployment

1. Create account on PythonAnywhere
2. Upload project files
3. Set up virtual environment
4. Configure WSGI file
5. Set environment variables
6. Initialize database
7. Reload web app

### Environment Variables

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///path/to/db
```

## Future Enhancements

- Email notifications
- Payment gateway integration
- Video upload functionality
- Discussion forums
- Quizzes and assessments
- Certificate generation
- Social media integration
- Advanced analytics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is created for educational purposes as part of the BIT233 Web Technology course.

## Contact

For questions or support, contact: support@learnhub.com

## Acknowledgments

- Flask Documentation
- Bootstrap Documentation
- Stack Overflow Community
- Texas College of Management & IT
  """

# ==================

# DEPLOYMENT GUIDE

# ==================

"""
DEPLOYMENT GUIDE FOR ONLINE LEARNING PLATFORM

=== OPTION 1: PythonAnywhere Deployment ===

1. Create PythonAnywhere Account

   - Go to www.pythonanywhere.com
   - Sign up for a free account

2. Upload Your Project

   - Use Git:
     $ git clone <your-repo-url>
   - Or upload as ZIP file

3. Create Virtual Environment
   $ mkvirtualenv --python=/usr/bin/python3.10 myenv
   $ workon myenv
   $ pip install -r requirements.txt

4. Initialize Database
   $ python init_db.py

5. Configure WSGI File
   - Go to Web tab
   - Edit WSGI configuration file
   - Add:

import sys
path = '/home/<username>/online-learning-platform'
if path not in sys.path:
sys.path.append(path)

from app import create_app
application = create_app()

6. Set Static Files

   - URL: /static/
   - Directory: /home/<username>/online-learning-platform/app/static/

7. Reload Web App

=== OPTION 2: Heroku Deployment ===

1. Install Heroku CLI
2. Create Procfile:
   web: gunicorn run:app

3. Add gunicorn to requirements.txt
   gunicorn==20.1.0

4. Create runtime.txt:
   python-3.10.0

5. Deploy:
   $ heroku login
   $ heroku create your-app-name
   $ git push heroku main
   $ heroku run python init_db.py

=== OPTION 3: Render Deployment ===

1. Create account on Render.com
2. Connect GitHub repository
3. Configure build command:
   pip install -r requirements.txt
4. Configure start command:
   gunicorn run:app
5. Add environment variables
6. Deploy

=== GitHub Pages (Frontend Only) ===

1. Create gh-pages branch
2. Push static HTML/CSS/JS files
3. Enable GitHub Pages in settings
4. Access at: https://username.github.io/repo-name

=== LOCAL DEVELOPMENT ===

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Initialize database
5. Run application:
   $ python run.py
6. Access at: http://localhost:5000

=== PRODUCTION CHECKLIST ===

- [ ] Change SECRET_KEY in config.py
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set DEBUG=False
- [ ] Configure proper error handling
- [ ] Set up logging
- [ ] Configure CORS if needed
- [ ] Set up backups
- [ ] Configure email service
- [ ] Set up monitoring
      """

# ==================

# TESTING GUIDE

# ==================

"""
TESTING GUIDE

=== Manual Testing Checklist ===

USER AUTHENTICATION:

- [ ] Register new student account
- [ ] Register new instructor account
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Logout functionality
- [ ] Password validation (min 8 characters)
- [ ] Email format validation
- [ ] Duplicate username/email prevention

STUDENT FUNCTIONALITY:

- [ ] View student dashboard
- [ ] Browse all courses
- [ ] Search courses by keyword
- [ ] Filter courses by category
- [ ] Filter courses by difficulty
- [ ] View course details
- [ ] Enroll in a course
- [ ] View enrolled courses
- [ ] Track course progress
- [ ] Edit profile information
- [ ] Upload profile picture

INSTRUCTOR FUNCTIONALITY:

- [ ] View instructor dashboard
- [ ] Create new course
- [ ] Edit existing course
- [ ] Delete course
- [ ] Upload course image
- [ ] Add lessons to course
- [ ] View enrolled students
- [ ] Publish/unpublish course

ADMIN FUNCTIONALITY:

- [ ] View admin dashboard
- [ ] View all users
- [ ] Filter users by role
- [ ] Delete users
- [ ] View all courses
- [ ] Delete courses
- [ ] View platform statistics

RESPONSIVE DESIGN:

- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768x1024)
- [ ] Test on mobile (375x667)
- [ ] Navigation menu collapse
- [ ] Form responsiveness
- [ ] Card layouts adjust properly

FORMS VALIDATION:

- [ ] Client-side validation works
- [ ] Server-side validation works
- [ ] Error messages display correctly
- [ ] Success messages display correctly
- [ ] Required fields enforced
- [ ] Field length limits enforced

BROWSER COMPATIBILITY:

- [ ] Chrome
- [ ] Firefox
- [ ] Safari
- [ ] Edge

=== Testing Tools ===

1. Browser DevTools
2. Responsive Design Mode
3. Network Tab (check for errors)
4. Console (check for JavaScript errors)
5. Lighthouse (performance audit)
   """
