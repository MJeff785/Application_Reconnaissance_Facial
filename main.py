from face_database_manager import FaceDatabase
from facial_recognition_ml import FacialRecognitionSystem
import os

def main():
    # Initialiser la base de données et traiter les images si nécessaire
    db = FaceDatabase()
    images_dir = "Images_visages"
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Créé le dossier {images_dir}. Veuillez y ajouter des images de visages.")
        return

    # Traiter les nouvelles images et les ajouter à la base de données
    print("Mise à jour de la base de données...")
    db.process_directory(images_dir)

    # Démarrer le système de reconnaissance faciale
    print("Démarrage du système de reconnaissance...")
    system = FacialRecognitionSystem()
    system.load_dataset()
    if system.train_model():
        system.run_recognition()
    else:
        print("Échec de l'entraînement du modèle")

if __name__ == "__main__":
    main()