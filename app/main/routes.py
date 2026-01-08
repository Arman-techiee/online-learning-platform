from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import Course, Enrollment, User
from app.forms import ProfileForm, ContactForm
import os
from werkzeug.utils import secure_filename

@bp.route('/')
@bp.route('/index')
def index():
    """Homepage with featured courses"""
    featured_courses = Course.query.filter_by(is_published=True).order_by(Course.created_at.desc()).limit(6).all()
    total_courses = Course.query.filter_by(is_published=True).count()
    total_students = User.query.filter_by(role='student').count()
    total_instructors = User.query.filter_by(role='instructor').count()
    
    return render_template('index.html', 
                         title='Home',
                         featured_courses=featured_courses,
                         total_courses=total_courses,
                         total_students=total_students,
                         total_instructors=total_instructors)

@bp.route('/student/dashboard')
@login_required
def student_dashboard():
    """Student dashboard"""
    if current_user.role != 'student':
        flash('Access denied. Students only.', 'danger')
        return redirect(url_for('main.index'))
    
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    enrolled_courses = [e.course for e in enrollments]
    
    return render_template('student/dashboard.html',
                         title='Student Dashboard',
                         enrollments=enrollments,
                         enrolled_courses=enrolled_courses)

@bp.route('/student/my-courses')
@login_required
def my_courses():
    """Student's enrolled courses"""
    if current_user.role != 'student':
        flash('Access denied.', 'danger')
        return redirect(url_for('main.index'))
    
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    return render_template('student/my_courses.html',
                         title='My Courses',
                         enrollments=enrollments)

@bp.route('/instructor/dashboard')
@login_required
def instructor_dashboard():
    """Instructor dashboard"""
    if current_user.role != 'instructor':
        flash('Access denied. Instructors only.', 'danger')
        return redirect(url_for('main.index'))
    
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    total_students = sum([course.enrollments.count() for course in courses])
    
    return render_template('instructor/dashboard.html',
                         title='Instructor Dashboard',
                         courses=courses,
                         total_students=total_students)

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data.lower()
        current_user.bio = form.bio.data
        
        # Handle profile picture upload
        if form.profile_pic.data:
            file = form.profile_pic.data
            filename = secure_filename(file.filename)
            filename = f"{current_user.id}_{filename}"
            filepath = os.path.join('app/static/uploads/profiles', filename)
            file.save(filepath)
            current_user.profile_pic = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    
    return render_template('profile.html', title='Profile', form=form)

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form"""
    form = ContactForm()
    
    if form.validate_on_submit():
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', title='Contact Us', form=form)