from app import create_app, db
from app.models import Course, Lesson

app = create_app()

with app.app_context():
    print("\n=== Quick Add Lesson ===\n")
    
    # Show all courses
    courses = Course.query.all()
    print("Available Courses:")
    for course in courses:
        lesson_count = Lesson.query.filter_by(course_id=course.id).count()
        print(f"{course.id}. {course.title} ({lesson_count} lessons)")
    
    # Get course ID
    course_id = int(input("\nEnter Course ID: "))
    course = Course.query.get(course_id)
    
    if not course:
        print("Course not found!")
        exit()
    
    # Get lesson details
    print(f"\nAdding lesson to: {course.title}")
    title = input("Lesson Title: ")
    content = input("Lesson Content (HTML allowed): ")
    
    # Get next order number
    last_lesson = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order.desc()).first()
    order = (last_lesson.order + 1) if last_lesson else 1
    
    duration = input(f"Duration in minutes (default 30): ") or "30"
    
    # Create lesson
    lesson = Lesson(
        course_id=course_id,
        title=title,
        content=content,
        order=order,
        duration=int(duration)
    )
    
    db.session.add(lesson)
    db.session.commit()
    
    print(f"\n✅ Lesson '{title}' added successfully!")
    print(f"   Order: {order}")
    print(f"   Duration: {duration} minutes\n")