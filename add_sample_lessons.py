from app import create_app, db
from app.models import Course, Lesson

app = create_app()

with app.app_context():
    print("\n=== Adding Sample Lessons ===\n")
    
    # Get all courses
    courses = Course.query.all()
    
    if not courses:
        print("No courses found! Create courses first.")
        exit()
    
    for course in courses:
        print(f"\nAdding lessons to: {course.title}")
        
        # Check if course already has lessons
        existing = Lesson.query.filter_by(course_id=course.id).first()
        if existing:
            print(f"  ⚠️  Course already has lessons. Skipping...")
            continue
        
        # Sample lessons based on course category
        if 'Web' in course.title or 'Web' in course.category:
            lessons = [
                {
                    'title': 'Introduction to HTML',
                    'content': '''
                    <h3>Welcome to HTML</h3>
                    <p>HTML (HyperText Markup Language) is the standard markup language for creating web pages.</p>
                    
                    <h4>What You'll Learn:</h4>
                    <ul>
                        <li>Basic HTML structure</li>
                        <li>Common HTML tags</li>
                        <li>Creating your first web page</li>
                    </ul>
                    
                    <h4>HTML Document Structure:</h4>
                    <pre>
&lt;!DOCTYPE html&gt;
&lt;html&gt;
  &lt;head&gt;
    &lt;title&gt;My Page&lt;/title&gt;
  &lt;/head&gt;
  &lt;body&gt;
    &lt;h1&gt;Hello World!&lt;/h1&gt;
  &lt;/body&gt;
&lt;/html&gt;
                    </pre>
                    
                    <h4>Practice Exercise:</h4>
                    <p>Create a simple HTML page with a heading and paragraph.</p>
                    ''',
                    'order': 1,
                    'duration': 30
                },
                {
                    'title': 'CSS Fundamentals',
                    'content': '''
                    <h3>Styling with CSS</h3>
                    <p>CSS (Cascading Style Sheets) is used to style and layout web pages.</p>
                    
                    <h4>CSS Syntax:</h4>
                    <pre>
selector {
    property: value;
}
                    </pre>
                    
                    <h4>Common Properties:</h4>
                    <ul>
                        <li>color - Text color</li>
                        <li>background-color - Background color</li>
                        <li>font-size - Text size</li>
                        <li>margin - Outer spacing</li>
                        <li>padding - Inner spacing</li>
                    </ul>
                    
                    <h4>Example:</h4>
                    <pre>
h1 {
    color: blue;
    font-size: 32px;
    text-align: center;
}
                    </pre>
                    ''',
                    'order': 2,
                    'duration': 45
                },
                {
                    'title': 'JavaScript Basics',
                    'content': '''
                    <h3>Introduction to JavaScript</h3>
                    <p>JavaScript brings interactivity to your web pages.</p>
                    
                    <h4>Variables:</h4>
                    <pre>
let name = "John";
const age = 25;
var city = "New York";
                    </pre>
                    
                    <h4>Functions:</h4>
                    <pre>
function greet(name) {
    return "Hello, " + name + "!";
}

console.log(greet("Alice"));
                    </pre>
                    
                    <h4>DOM Manipulation:</h4>
                    <pre>
document.getElementById("myButton").addEventListener("click", function() {
    alert("Button clicked!");
});
                    </pre>
                    ''',
                    'order': 3,
                    'duration': 60
                }
            ]
        
        elif 'Python' in course.title or 'Python' in course.category:
            lessons = [
                {
                    'title': 'Python Basics',
                    'content': '''
                    <h3>Getting Started with Python</h3>
                    <p>Python is a powerful, easy-to-learn programming language.</p>
                    
                    <h4>Variables and Data Types:</h4>
                    <pre>
# Numbers
age = 25
price = 99.99

# Strings
name = "John Doe"
message = 'Hello, World!'

# Boolean
is_student = True
                    </pre>
                    
                    <h4>Basic Operations:</h4>
                    <pre>
# Arithmetic
result = 10 + 5
print(result)  # 15

# String concatenation
greeting = "Hello" + " " + "World"
print(greeting)  # Hello World
                    </pre>
                    ''',
                    'order': 1,
                    'duration': 40
                },
                {
                    'title': 'Control Flow',
                    'content': '''
                    <h3>If Statements and Loops</h3>
                    
                    <h4>If Statements:</h4>
                    <pre>
age = 18

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")
                    </pre>
                    
                    <h4>For Loops:</h4>
                    <pre>
for i in range(5):
    print(i)

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
                    </pre>
                    
                    <h4>While Loops:</h4>
                    <pre>
count = 0
while count < 5:
    print(count)
    count += 1
                    </pre>
                    ''',
                    'order': 2,
                    'duration': 45
                }
            ]
        
        else:
            # Generic lessons for other courses
            lessons = [
                {
                    'title': 'Course Introduction',
                    'content': '''
                    <h3>Welcome to the Course!</h3>
                    <p>In this course, you will learn essential concepts and practical skills.</p>
                    
                    <h4>Course Objectives:</h4>
                    <ul>
                        <li>Understand fundamental concepts</li>
                        <li>Apply knowledge in practical scenarios</li>
                        <li>Build real-world projects</li>
                    </ul>
                    
                    <h4>What You Need:</h4>
                    <ul>
                        <li>Basic computer skills</li>
                        <li>Willingness to learn</li>
                        <li>Practice regularly</li>
                    </ul>
                    ''',
                    'order': 1,
                    'duration': 20
                },
                {
                    'title': 'Core Concepts',
                    'content': '''
                    <h3>Understanding the Fundamentals</h3>
                    <p>Let's dive into the core concepts you need to master.</p>
                    
                    <h4>Key Topics:</h4>
                    <ol>
                        <li>Foundation principles</li>
                        <li>Best practices</li>
                        <li>Common patterns</li>
                        <li>Real-world applications</li>
                    </ol>
                    
                    <h4>Learning Approach:</h4>
                    <p>We'll use a hands-on approach with practical examples and exercises.</p>
                    ''',
                    'order': 2,
                    'duration': 40
                }
            ]
        
        # Add lessons to database
        for lesson_data in lessons:
            lesson = Lesson(
                course_id=course.id,
                title=lesson_data['title'],
                content=lesson_data['content'],
                order=lesson_data['order'],
                duration=lesson_data.get('duration', 30)
            )
            db.session.add(lesson)
            print(f"  ✓ Added: {lesson_data['title']}")
        
        db.session.commit()
    
    print("\n✅ Sample lessons added successfully!\n")
