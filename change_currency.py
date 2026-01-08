import os

files = [
    'app/templates/index.html',
    'app/templates/courses/browse.html',
    'app/templates/courses/detail.html',
    'app/templates/instructor/create_course.html',
    'app/templates/instructor/edit_course.html',
    'app/templates/admin/courses.html',
]

for filepath in files:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace $ with Rs.
        content = content.replace('${{', 'Rs. {{')
        content = content.replace('<span class="input-group-text">$</span>', 
                                 '<span class="input-group-text">Rs.</span>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {filepath}")

print("\n✅ All files updated! Currency changed to Rs.")
print("Refresh your browser to see changes!")