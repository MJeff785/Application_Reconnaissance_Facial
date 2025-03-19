import cv2
import face_recognition
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from face_database_manager import FaceDatabase

class FacialRecognitionSystem:
    def __init__(self, dataset_path="Images_visages"):
        self.dataset_path = dataset_path
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_classifier = SVC(kernel='linear', probability=True)
        self.le = LabelEncoder()
        self.db = FaceDatabase()
        
    def load_dataset(self):
        print("Chargement des encodages depuis la base de données...")
        self.known_face_encodings, self.known_face_names = self.db.get_all_faces()
        if self.known_face_encodings:
            print(f"Chargé {len(self.known_face_encodings)} visages")
        else:
            print("Aucun visage trouvé dans la base de données")

    def train_model(self):
        if len(self.known_face_encodings) == 0:
            print("Aucune donnée d'entraînement disponible")
            return False
            
        print("Entraînement du modèle...")
        # Add a dummy class if only one person is present
        if len(set(self.known_face_names)) == 1:
            self.known_face_encodings.append(np.zeros_like(self.known_face_encodings[0]))
            self.known_face_names.append("dummy_class")
            
        encoded_labels = self.le.fit_transform(self.known_face_names)
        self.face_classifier.fit(self.known_face_encodings, encoded_labels)
        return True

    def run_recognition(self):
        print("Démarrage de la reconnaissance faciale...")
        video_capture = cv2.VideoCapture(0)

        # Optimiser la résolution
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Redimensionner pour la détection
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Détection des visages
            face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")

            # Ne traiter que si un visage est détecté
            if face_locations:
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # Ajuster les coordonnées
                    top *= 2
                    right *= 2
                    bottom *= 2
                    left *= 2

                    # Prédiction uniquement si un visage est détecté
                    predictions = self.face_classifier.predict_proba([face_encoding])[0]
                    best_match_index = np.argmax(predictions)
                    confidence = predictions[best_match_index]
                    
                    if confidence > 0.6:
                        name = self.le.inverse_transform([best_match_index])[0]
                        label = f"{name} ({confidence*100:.1f}%)"
                    else:
                        label = "Inconnu"

                    # Dessiner uniquement si un visage est détecté
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, label, (left + 6, bottom - 6), 
                              cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

            # Afficher le frame
            cv2.imshow('Reconnaissance Faciale', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

def main():
    # Créer le dossier des images s'il n'existe pas
    if not os.path.exists("Images_visages"):
        os.makedirs("Images_visages")
        print("Dossier Images_visages créé. Veuillez y ajouter des images de visages.")
        return

    # Initialiser et exécuter le système
    system = FacialRecognitionSystem()
    system.load_dataset()
    if system.train_model():
        system.run_recognition()
    else:
        print("Échec de l'entraînement du modèle")

if __name__ == "__main__":
    main()