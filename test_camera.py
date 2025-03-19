import cv2

def test_camera():
    # Try different camera indices
    for index in range(3):
        print(f"Trying camera index {index}...")
        cap = cv2.VideoCapture(index)
        
        if not cap.isOpened():
            print(f"Could not open camera {index}")
            continue
            
        ret, frame = cap.read()
        if ret:
            print(f"Successfully captured frame from camera {index}")
            cv2.imshow(f'Camera Test {index}', frame)
            cv2.waitKey(2000)  # Show for 2 seconds
        else:
            print(f"Could not read frame from camera {index}")
            
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()