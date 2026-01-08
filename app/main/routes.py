from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.models import Course, Enrollment, User
from app.forms import ProfileForm, ContactForm
from app.forms import CourseForm, LessonForm
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
        # Here you would typically send an email
        flash('Thank you for contacting us! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', title='Contact Us', form=form)
@bp.route('/<int:course_id>/lessons/add', methods=['GET', 'POST'])
@login_required
def add_lesson(course_id):
    """Add a new lesson to a course (instructors only)"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user owns this course
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    form = LessonForm()
    
    if form.validate_on_submit():
        # Get next lesson order number
        last_lesson = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order.desc()).first()
        next_order = (last_lesson.order + 1) if last_lesson else 1
        
        lesson = Lesson(
            course_id=course_id,
            title=form.title.data,
            content=form.content.data,
            order=form.order.data or next_order,
            video_url=form.video_url.data,
            duration=form.duration.data
        )
        
        db.session.add(lesson)
        db.session.commit()
        flash('Lesson added successfully!', 'success')
        return redirect(url_for('courses.manage_lessons', course_id=course_id))
    
    # Pre-fill order number
    last_lesson = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order.desc()).first()
    next_order = (last_lesson.order + 1) if last_lesson else 1
    form.order.data = next_order
    
    return render_template('courses/add_lesson.html', 
                         title='Add Lesson',
                         form=form,
                         course=course)


# NEW ROUTE: Manage Course Lessons
@bp.route('/<int:course_id>/lessons', methods=['GET'])
@login_required
def manage_lessons(course_id):
    """View and manage all lessons for a course"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user owns this course
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()
    
    return render_template('courses/manage_lessons.html',
                         title='Manage Lessons',
                         course=course,
                         lessons=lessons)


# NEW ROUTE: Edit Lesson
@bp.route('/lessons/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lesson(lesson_id):
    """Edit an existing lesson"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    # Check if user owns this course
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    form = LessonForm()
    
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.content = form.content.data
        lesson.order = form.order.data
        lesson.video_url = form.video_url.data
        lesson.duration = form.duration.data
        
        db.session.commit()
        flash('Lesson updated successfully!', 'success')
        return redirect(url_for('courses.manage_lessons', course_id=course.id))
    
    elif request.method == 'GET':
        form.title.data = lesson.title
        form.content.data = lesson.content
        form.order.data = lesson.order
        form.video_url.data = lesson.video_url
        form.duration.data = lesson.duration
    
    return render_template('courses/edit_lesson.html',
                         title='Edit Lesson',
                         form=form,
                         lesson=lesson,
                         course=course)


# NEW ROUTE: Delete Lesson
@bp.route('/lessons/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    """Delete a lesson"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    # Check if user owns this course
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    course_id = course.id
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted successfully.', 'success')
    
    return redirect(url_for('courses.manage_lessons', course_id=course_id))


# NEW ROUTE: View Lesson (for students)
@bp.route('/lessons/<int:lesson_id>')
@login_required
def view_lesson(lesson_id):
    """View lesson content (students and instructors)"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    # Check if student is enrolled or if user is instructor/admin
    if current_user.role == 'student':
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            course_id=course.id
        ).first()
        
        if not enrollment:
            flash('You must be enrolled in this course to view lessons.', 'warning')
            return redirect(url_for('courses.detail', course_id=course.id))
    elif current_user.role == 'instructor':
        if course.instructor_id != current_user.id:
            abort(403)
    
    # Get all lessons for navigation
    all_lessons = Lesson.query.filter_by(course_id=course.id).order_by(Lesson.order).all()
    
    # Find previous and next lessons
    current_index = all_lessons.index(lesson)
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None
    
    return render_template('courses/view_lesson.html',
                         title=lesson.title,
                         lesson=lesson,
                         course=course,
                         all_lessons=all_lessons,
                         prev_lesson=prev_lesson,
                         next_lesson=next_lesson)

