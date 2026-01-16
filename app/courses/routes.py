# app/courses/routes.py
"""
Complete routes for course and lesson management
Includes CRUD operations for courses and lessons, plus progress tracking and PDF support
"""

from flask import render_template, redirect, url_for, flash, request, abort, jsonify, send_from_directory
from flask_login import login_required, current_user
from app import db
from app.courses import bp
from app.models import Course, Lesson, Enrollment, LessonProgress
from app.forms import CourseForm, LessonForm
from datetime import datetime
import os
from werkzeug.utils import secure_filename


# ============================================================================
# COURSE ROUTES
# ============================================================================

@bp.route('/browse')
def browse():
    """Browse all published courses with filters and pagination"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    difficulty = request.args.get('difficulty', 'all')
    search = request.args.get('search', '')
    
    # Base query - only published courses
    query = Course.query.filter_by(is_published=True)
    
    # Apply filters
    if category != 'all':
        query = query.filter_by(category=category)
    if difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (Course.title.ilike(search_filter)) | 
            (Course.description.ilike(search_filter))
        )
    
    # Paginate results
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
    """Course detail page with enrollment check"""
    course = Course.query.get_or_404(course_id)
    
    # Check if user is enrolled
    is_enrolled = False
    if current_user.is_authenticated:
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            course_id=course_id
        ).first()
        is_enrolled = enrollment is not None
    
    # Get all lessons ordered by sequence
    lessons = course.lessons.order_by(Lesson.order).all()
    
    return render_template('courses/detail.html',
                         title=course.title,
                         course=course,
                         lessons=lessons,
                         is_enrolled=is_enrolled)


@bp.route('/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    """Enroll student in a course"""
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
        # Create enrollment
        enrollment = Enrollment(
            student_id=current_user.id, 
            course_id=course_id,
            progress=0,
            completed=False
        )
        db.session.add(enrollment)
        db.session.commit()
        
        # Initialize lesson progress for all lessons
        lessons = course.lessons.all()
        for lesson in lessons:
            lesson_progress = LessonProgress(
                enrollment_id=enrollment.id,
                lesson_id=lesson.id,
                completed=False
            )
            db.session.add(lesson_progress)
        
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
            filename = f"course_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join('app/static/uploads/courses', filename)
            file.save(filepath)
            course.image = filename
        
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully! Now add lessons to your course.', 'success')
        return redirect(url_for('courses.manage_lessons', course_id=course.id))
    
    return render_template('instructor/create_course.html',
                         title='Create Course',
                         form=form)


@bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(course_id):
    """Edit a course"""
    course = Course.query.get_or_404(course_id)
    
    # Check permissions
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
        
        # Handle image upload
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            filename = f"course_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join('app/static/uploads/courses', filename)
            file.save(filepath)
            course.image = filename
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('courses.detail', course_id=course.id))
    
    elif request.method == 'GET':
        # Pre-populate form
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
    
    # Check permissions
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully.', 'success')
    
    # Redirect based on user role
    if current_user.role == 'admin':
        return redirect(url_for('admin.courses'))
    return redirect(url_for('main.instructor_dashboard'))


# ============================================================================
# LESSON MANAGEMENT ROUTES (INSTRUCTOR)
# ============================================================================

@bp.route('/<int:course_id>/lessons/manage')
@login_required
def manage_lessons(course_id):
    """View and manage all lessons for a course"""
    course = Course.query.get_or_404(course_id)
    
    # Check permissions
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()
    
    return render_template('courses/manage_lessons.html',
                         title='Manage Lessons',
                         course=course,
                         lessons=lessons)


@bp.route('/<int:course_id>/lessons/add', methods=['GET', 'POST'])
@login_required
def add_lesson(course_id):
    """Add a new lesson to a course"""
    course = Course.query.get_or_404(course_id)
    
    # Check permissions
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    form = LessonForm()
    
    if form.validate_on_submit():
        lesson = Lesson(
            course_id=course_id,
            title=form.title.data,
            content=form.content.data,
            order=form.order.data,
            video_url=form.video_url.data,
            duration=form.duration.data
        )
        
        # Handle PDF upload
        if form.pdf_file.data:
            file = form.pdf_file.data
            filename = secure_filename(file.filename)
            filename = f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join('app/static/uploads/pdfs', filename)
            
            # Create pdfs folder if it doesn't exist
            os.makedirs('app/static/uploads/pdfs', exist_ok=True)
            
            file.save(filepath)
            lesson.pdf_file = filename
        
        db.session.add(lesson)
        db.session.commit()
        
        # Create lesson progress entries for all enrolled students
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        for enrollment in enrollments:
            lesson_progress = LessonProgress(
                enrollment_id=enrollment.id,
                lesson_id=lesson.id,
                completed=False
            )
            db.session.add(lesson_progress)
        
        db.session.commit()
        flash('Lesson added successfully!', 'success')
        return redirect(url_for('courses.manage_lessons', course_id=course_id))
    
    # Pre-fill order number with next available
    last_lesson = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order.desc()).first()
    next_order = (last_lesson.order + 1) if last_lesson else 1
    form.order.data = next_order
    
    return render_template('courses/add_lesson.html', 
                         title='Add Lesson',
                         form=form,
                         course=course)


@bp.route('/lessons/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_lesson(lesson_id):
    """Edit an existing lesson"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    # Check permissions
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    form = LessonForm()
    
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.content = form.content.data
        lesson.order = form.order.data
        lesson.video_url = form.video_url.data
        lesson.duration = form.duration.data
        
        # Handle PDF upload
        if form.pdf_file.data:
            # Delete old PDF if exists
            if lesson.pdf_file:
                old_filepath = os.path.join('app/static/uploads/pdfs', lesson.pdf_file)
                if os.path.exists(old_filepath):
                    try:
                        os.remove(old_filepath)
                    except Exception as e:
                        print(f"Error deleting old PDF: {e}")
            
            # Save new PDF
            file = form.pdf_file.data
            filename = secure_filename(file.filename)
            filename = f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join('app/static/uploads/pdfs', filename)
            
            # Create pdfs folder if it doesn't exist
            os.makedirs('app/static/uploads/pdfs', exist_ok=True)
            
            file.save(filepath)
            lesson.pdf_file = filename
        
        db.session.commit()
        flash('Lesson updated successfully!', 'success')
        return redirect(url_for('courses.manage_lessons', course_id=course.id))
    
    elif request.method == 'GET':
        # Pre-populate form
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


@bp.route('/lessons/<int:lesson_id>/delete', methods=['POST'])
@login_required
def delete_lesson(lesson_id):
    """Delete a lesson"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    # Check permissions
    if course.instructor_id != current_user.id and current_user.role != 'admin':
        abort(403)
    
    # Delete associated PDF if exists
    if lesson.pdf_file:
        pdf_filepath = os.path.join('app/static/uploads/pdfs', lesson.pdf_file)
        if os.path.exists(pdf_filepath):
            try:
                os.remove(pdf_filepath)
            except Exception as e:
                print(f"Error deleting PDF: {e}")
    
    course_id = course.id
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted successfully.', 'success')
    
    return redirect(url_for('courses.manage_lessons', course_id=course_id))


# ============================================================================
# PDF DOWNLOAD ROUTE
# ============================================================================

@bp.route('/lessons/<int:lesson_id>/download-pdf')
@login_required
def download_pdf(lesson_id):
    """Download/view lesson PDF"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    # Check if user has access (enrolled student, instructor, or admin)
    has_access = False
    
    if current_user.role == 'admin':
        has_access = True
    elif current_user.id == course.instructor_id:
        has_access = True
    elif current_user.role == 'student':
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            course_id=course.id
        ).first()
        has_access = enrollment is not None
    
    if not has_access:
        flash('You must be enrolled in this course to access lesson materials.', 'danger')
        abort(403)
    
    if not lesson.pdf_file:
        flash('No PDF attachment found for this lesson.', 'warning')
        return redirect(url_for('courses.view_lesson', lesson_id=lesson_id))
    
    # Construct the full file path
    pdf_directory = os.path.join(os.getcwd(), 'app', 'static', 'uploads', 'pdfs')
    pdf_path = os.path.join(pdf_directory, lesson.pdf_file)
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        flash(f'PDF file not found on server.', 'danger')
        return redirect(url_for('courses.view_lesson', lesson_id=lesson_id))
    
    # Serve the PDF file
    try:
        return send_from_directory(pdf_directory, lesson.pdf_file, as_attachment=False)
    except Exception as e:
        flash(f'Error loading PDF: {str(e)}', 'danger')
        return redirect(url_for('courses.view_lesson', lesson_id=lesson_id))


# ============================================================================
# LESSON VIEWING & PROGRESS TRACKING (STUDENT)
# ============================================================================

@bp.route('/lessons/<int:lesson_id>/view')
@login_required
def view_lesson(lesson_id):
    """View lesson content with progress tracking"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    # Check permissions and enrollment
    enrollment = None
    is_completed = False
    lesson_completion_status = {}
    
    if current_user.role == 'student':
        enrollment = Enrollment.query.filter_by(
            student_id=current_user.id,
            course_id=course.id
        ).first()
        
        if not enrollment:
            flash('You must be enrolled in this course to view lessons.', 'warning')
            return redirect(url_for('courses.detail', course_id=course.id))
        
        # Get lesson progress
        lesson_progress = LessonProgress.query.filter_by(
            enrollment_id=enrollment.id,
            lesson_id=lesson.id
        ).first()
        
        is_completed = lesson_progress.completed if lesson_progress else False
        
        # Get completion status for all lessons (for sidebar)
        all_lessons = Lesson.query.filter_by(course_id=course.id).order_by(Lesson.order).all()
        for l in all_lessons:
            prog = LessonProgress.query.filter_by(
                enrollment_id=enrollment.id,
                lesson_id=l.id
            ).first()
            lesson_completion_status[l.id] = prog.completed if prog else False
        
    elif current_user.role == 'instructor':
        if course.instructor_id != current_user.id:
            abort(403)
        all_lessons = Lesson.query.filter_by(course_id=course.id).order_by(Lesson.order).all()
    elif current_user.role == 'admin':
        all_lessons = Lesson.query.filter_by(course_id=course.id).order_by(Lesson.order).all()
    else:
        abort(403)
    
    # Get navigation lessons
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
                         next_lesson=next_lesson,
                         is_completed=is_completed,
                         lesson_completion_status=lesson_completion_status,
                         enrollment=enrollment)


@bp.route('/lessons/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    """Mark a lesson as completed (AJAX endpoint)"""
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course
    
    if current_user.role != 'student':
        return jsonify({
            'success': False, 
            'message': 'Only students can complete lessons'
        }), 403
    
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        return jsonify({
            'success': False, 
            'message': 'Not enrolled in this course'
        }), 403
    
    # Get or create lesson progress
    lesson_progress = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        lesson_id=lesson.id
    ).first()
    
    if not lesson_progress:
        lesson_progress = LessonProgress(
            enrollment_id=enrollment.id,
            lesson_id=lesson.id,
            completed=True,
            completed_at=datetime.utcnow()
        )
        db.session.add(lesson_progress)
    else:
        if not lesson_progress.completed:
            lesson_progress.completed = True
            lesson_progress.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    # Calculate and update course progress
    new_progress = calculate_course_progress(enrollment)
    enrollment.progress = new_progress
    
    # Mark course as completed if 100%
    if new_progress >= 100:
        enrollment.completed = True
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'progress': new_progress,
        'completed': enrollment.completed,
        'message': 'Lesson marked as complete!'
    })


@bp.route('/<int:course_id>/progress')
@login_required
def course_progress(course_id):
    """View detailed course progress"""
    course = Course.query.get_or_404(course_id)
    
    if current_user.role != 'student':
        flash('Only students can view progress.', 'danger')
        return redirect(url_for('courses.detail', course_id=course_id))
    
    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        course_id=course.id
    ).first()
    
    if not enrollment:
        flash('You must be enrolled in this course.', 'warning')
        return redirect(url_for('courses.detail', course_id=course_id))
    
    # Get all lessons with completion status
    lessons = course.lessons.order_by(Lesson.order).all()
    lesson_data = []
    
    for lesson in lessons:
        progress = LessonProgress.query.filter_by(
            enrollment_id=enrollment.id,
            lesson_id=lesson.id
        ).first()
        
        lesson_data.append({
            'lesson': lesson,
            'completed': progress.completed if progress else False,
            'completed_at': progress.completed_at if progress else None
        })
    
    return render_template('courses/progress.html',
                         title='Course Progress',
                         course=course,
                         enrollment=enrollment,
                         lesson_data=lesson_data)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_course_progress(enrollment):
    """Calculate accurate course progress based on completed lessons"""
    course = enrollment.course
    total_lessons = course.lessons.count()
    
    if total_lessons == 0:
        return 0
    
    completed_lessons = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id,
        completed=True
    ).count()
    
    progress = int((completed_lessons / total_lessons) * 100)
    
    return progress