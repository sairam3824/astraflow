#!/usr/bin/env python3
"""
Migration script to add first_name and last_name columns to users table
"""
import sqlite3
import sys
from pathlib import Path

def migrate():
    db_path = Path("data/astraflow.db")
    
    if not db_path.exists():
        print("Database doesn't exist yet. Will be created with new schema.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'first_name' in columns and 'last_name' in columns:
            print("✓ Columns already exist. No migration needed.")
            return
        
        # Add first_name column if it doesn't exist
        if 'first_name' not in columns:
            print("Adding first_name column...")
            cursor.execute("ALTER TABLE users ADD COLUMN first_name TEXT")
            print("✓ Added first_name column")
        
        # Add last_name column if it doesn't exist
        if 'last_name' not in columns:
            print("Adding last_name column...")
            cursor.execute("ALTER TABLE users ADD COLUMN last_name TEXT")
            print("✓ Added last_name column")
        
        conn.commit()
        print("\n✓ Migration completed successfully!")
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        conn.rollback()
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
