"""
Migration script to add pdf_file column to lessons table
Run this after updating the models
"""

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Adding pdf_file column to lessons table...")
    
    try:
        # Check if column already exists
        result = db.session.execute(text("PRAGMA table_info(lessons)"))
        columns = [row[1] for row in result]
        
        if 'pdf_file' not in columns:
            # Add the column
            db.session.execute(text("ALTER TABLE lessons ADD COLUMN pdf_file VARCHAR(255)"))
            db.session.commit()
            print("✅ Successfully added pdf_file column to lessons table!")
        else:
            print("ℹ️  pdf_file column already exists in lessons table")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()