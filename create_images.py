from PIL import Image, ImageDraw, ImageFont

# Create default profile image (200x200)
def create_profile_image():
    img = Image.new('RGB', (200, 200), color='#0D6EFD')
    d = ImageDraw.Draw(img)
    
    # Draw text
    text = "USER"
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # Get text size and center it
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((200 - text_width) // 2, (200 - text_height) // 2)
    
    d.text(position, text, fill='white', font=font)
    img.save('app/static/images/default.jpg')
    print("✓ Created default.jpg")

# Create default course image (400x300)
def create_course_image():
    img = Image.new('RGB', (400, 300), color='#0D6EFD')
    d = ImageDraw.Draw(img)
    
    # Draw text
    text = "COURSE"
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()
    
    # Get text size and center it
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((400 - text_width) // 2, (300 - text_height) // 2)
    
    d.text(position, text, fill='white', font=font)
    img.save('app/static/images/default_course.jpg')
    print("✓ Created default_course.jpg")

# Create hero illustration (800x400)
def create_hero_image():
    img = Image.new('RGB', (800, 400), color='#667eea')
    d = ImageDraw.Draw(img)
    
    # Draw text
    text = "LearnHub"
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Get text size and center it
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((800 - text_width) // 2, (400 - text_height) // 2)
    
    d.text(position, text, fill='white', font=font)
    img.save('app/static/images/hero-illustration.jpg')
    print("✓ Created hero-illustration.jpg")

if __name__ == "__main__":
    print("Creating default images...")
    create_profile_image()
    create_course_image()
    create_hero_image()
    print("\n✓ All images created successfully!")
    print("Location: app/static/images/")