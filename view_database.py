
import sqlite3
import pickle
import numpy as np

def view_database():
    conn = sqlite3.connect('face_encodings.db')
    cursor = conn.cursor()
    
    print("\n=== Face Encodings Database Content ===")
    cursor.execute("SELECT * FROM face_encodings")
    rows = cursor.fetchall()
    
    if not rows:
        print("Database is empty!")
    else:
        print(f"\nTotal entries: {len(rows)}")
        print("\nEntries:")
        print("-" * 100)
        for row in rows:
            id, name, encoding_blob, path = row
            encoding = pickle.loads(encoding_blob)
            print(f"ID: {id}")
            print(f"Name: {name}")
            print(f"Image Path: {path}")
            print(f"Face Encoding (first 5 values): {encoding[:5]}")
            print("-" * 100)
    
    conn.close()

if __name__ == "__main__":
    view_database()