import face_recognition
import numpy as np
import cv2

def show_face_measurements(image_path):
    # Load image
    image = face_recognition.load_image_file(image_path)
    
    # Get face locations
    face_locations = face_recognition.face_locations(image)
    
    if not face_locations:
        print("No face detected in the image!")
        return
    
    # Get facial landmarks
    face_landmarks = face_recognition.face_landmarks(image)
    face_encoding = face_recognition.face_encodings(image)[0]
    
    print("\n=== Face Measurements ===")
    print(f"\nNumber of measurements: {len(face_encoding)}")
    print("\nFacial encoding values (128 measurements):")
    for i, value in enumerate(face_encoding):
        print(f"Measurement {i+1}: {value:.6f}")
    
    # Display image with landmarks
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Draw landmarks
    for landmarks in face_landmarks:
        for feature in landmarks.values():
            for point in feature:
                cv2.circle(image_rgb, point, 2, (0, 255, 0), -1)
    
    # Show image with landmarks
    cv2.imshow('Facial Landmarks', image_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Example usage
    image_path = input("Enter the path to your image: ")
    show_face_measurements(image_path)