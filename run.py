from app import create_app, db
from app.models import User, Course, Enrollment, Lesson, Assignment

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Course': Course,
        'Enrollment': Enrollment,
        'Lesson': Lesson,
        'Assignment': Assignment
    }

if __name__ == '__main__':
    app.run(debug=True)