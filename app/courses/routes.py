from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.courses import bp
from app.models import Course, Lesson, Enrollment
from app.forms import CourseForm, LessonForm
import os
from werkzeug.utils import secure_filename

@bp.route('/browse')
def browse():
    """Browse all published courses"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    difficulty = request.args.get('difficulty', 'all')
    search = request.args.get('search', '')
    
    query = Course.query.filter_by(is_published=True)
    
    # Apply filters
    if category != 'all':
        query = query.filter_by(category=category)
    if difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
    if search:
        query = query.filter(Course.title.contains(search) | Course.description.contains(search))
    
    courses = query.order_by(Course.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    
    return render_template('courses/browse.html',
                         title='Browse Courses',
                         courses=courses,
                         category=category,
                         difficulty=difficulty,
                         search=search)

@bp.route('/<int:course_id>')
def detail(course_id):
    """Course detail page"""
    course = Course.query.get_or_404(course_id)
    
    is_enrolled = False
    if current_user.is_authenticated:
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            course_id=course_id
        ).first()
        is_enrolled = enrollment is not None
    
    lessons = course.lessons.order_by(Lesson.order).all()
    
    return render_template('courses/detail.html',
                         title=course.title,
                         course=course,
                         lessons=lessons,
                         is_enrolled=is_enrolled)

@bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    """Enroll in a course"""
    if current_user.role != 'student':
        flash('Only students can enroll in courses.', 'danger')
        return redirect(url_for('courses.detail', course_id=course_id))
    
    course = Course.query.get_or_404(course_id)
    
    # Check if already enrolled
    existing = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()
    
    if existing:
        flash('You are already enrolled in this course.', 'info')
    else:
        enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash(f'Successfully enrolled in {course.title}!', 'success')
    
    return redirect(url_for('courses.detail', course_id=course_id))

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create a new course (instructors only)"""
    if current_user.role != 'instructor':
        flash('Only instructors can create courses.', 'danger')
        return redirect(url_for('main.index'))
    
    form = CourseForm()
    
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            price=form.price.data,
            difficulty=form.difficulty.data,
            instructor_id=current_user.id,
            is_published=form.is_published.data
        )
        
        # Handle course image upload
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            filename = f"course_{filename}"
            filepath = os.path.join('app/static/uploads/courses', filename)
            file.save(filepath)
            course.image = filename
        
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('main.instructor_dashboard'))
    
    return render_template('instructor/create_course.html',
                         title='Create Course',
                         form=form)

@bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(course_id):
    """Edit a course"""
    course = Course.query.get_or_404(course_id)
    
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    form = CourseForm()
    
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        course.category = form.category.data
        course.price = form.price.data
        course.difficulty = form.difficulty.data
        course.is_published = form.is_published.data
        
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            filename = f"course_{filename}"
            filepath = os.path.join('app/static/uploads/courses', filename)
            file.save(filepath)
            course.image = filename
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('courses.detail', course_id=course.id))
    
    elif request.method == 'GET':
        form.title.data = course.title
        form.description.data = course.description
        form.category.data = course.category
        form.price.data = course.price
        form.difficulty.data = course.difficulty
        form.is_published.data = course.is_published
    
    return render_template('instructor/edit_course.html',
                         title='Edit Course',
                         form=form,
                         course=course)

@bp.route('/<int:course_id>/delete', methods=['POST'])
@login_required
def delete(course_id):
    """Delete a course"""
    course = Course.query.get_or_404(course_id)
    
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully.', 'success')
    
    if current_user.role == 'admin':
        return redirect(url_for('admin.courses'))
    return redirect(url_for('main.instructor_dashboard'))