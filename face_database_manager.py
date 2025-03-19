import face_recognition
import os
import sqlite3
import numpy as np
import pickle

class FaceDatabase:
    def __init__(self, db_path="face_encodings.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS face_encodings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                encoding BLOB NOT NULL,
                image_path TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def add_face(self, image_path, name):
        try:
            # Check if image already exists in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM face_encodings WHERE image_path = ?", (image_path,))
            existing = cursor.fetchone()
            
            if existing:
                print(f"Image already exists in database: {image_path}")
                conn.close()
                return False
            
            # Load and encode the face
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if not face_encodings:
                print(f"No face found in {image_path}")
                conn.close()
                # Delete the image file
                try:
                    os.remove(image_path)
                    print(f"Image deleted: {image_path}")
                except Exception as e:
                    print(f"Error deleting image: {e}")
                return False
            
            # Serialize the encoding
            encoding_bytes = pickle.dumps(face_encodings[0])
            
            # Save to database
            cursor.execute(
                "INSERT INTO face_encodings (name, encoding, image_path) VALUES (?, ?, ?)",
                (name, encoding_bytes, image_path)
            )
            conn.commit()
            conn.close()
            print(f"Successfully added face encoding for {name} from {image_path}")
            return True
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return False

    def get_all_faces(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, encoding FROM face_encodings")
        results = cursor.fetchall()
        conn.close()

        face_encodings = []
        face_names = []
        for name, encoding_bytes in results:
            face_encodings.append(pickle.loads(encoding_bytes))
            face_names.append(name)
        
        return face_encodings, face_names

    def process_directory(self, directory_path):
        for person_name in os.listdir(directory_path):
            person_dir = os.path.join(directory_path, person_name)
            if os.path.isdir(person_dir):
                for image_name in os.listdir(person_dir):
                    if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(person_dir, image_name)
                        self.add_face(image_path, person_name)

def main():
    # Example usage
    db = FaceDatabase()
    images_dir = "Images_visages"
    
    if os.path.exists(images_dir):
        print("Processing images directory...")
        db.process_directory(images_dir)
        print("Finished processing images")
    else:
        print(f"Directory {images_dir} not found")

if __name__ == "__main__":
    main()