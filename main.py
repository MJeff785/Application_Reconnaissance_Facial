from face_database_manager import FaceDatabase
from facial_recognition_ml import FacialRecognitionSystem
import os
import tkinter as tk
from tkinter import messagebox

class FaceRecognitionApp:
    def __init__(self):
        self.db = FaceDatabase()
        self.system = None
        self.root = tk.Tk()
        self.root.title("Système de Reconnaissance Faciale")
        self.setup_gui()

    def setup_gui(self):
        # Main frame for buttons
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(expand=True)
        self.setup_main_buttons()
        
    def setup_main_buttons(self):
        # Add image button
        add_button = tk.Button(
            self.main_frame,
            text="Ajouter un visage",
            command=self.add_face,
            font=('Arial', 12),
            bg='#2196F3',
            fg='white',
            padx=20,
            pady=10
        )
        add_button.pack(pady=20)

        # View database button
        view_button = tk.Button(
            self.main_frame,
            text="Afficher la base de données",
            command=self.view_database,
            font=('Arial', 12),
            bg='#FF9800',
            fg='white',
            padx=20,
            pady=10
        )
        view_button.pack(pady=20)

        # Recognition button
        start_button = tk.Button(
            self.main_frame,
            text="Activer Reconnaissance",
            command=self.start_recognition,
            font=('Arial', 12),
            bg='#4CAF50',
            fg='white',
            padx=20,
            pady=10
        )
        start_button.pack(pady=20)

    def show_main_buttons(self):
        self.main_frame.pack(expand=True)

    def view_database(self):
        self.main_frame.pack_forget()
        from database_viewer import DatabaseViewer
        self.db_viewer = DatabaseViewer(self.root, self)  # Pass self as app reference
        self.db_viewer.show()

    def add_face(self):
        from image_manager_gui import ImageManagerWindow
        ImageManagerWindow(self.root)

    def start_recognition(self):
        self.root.destroy()  # Close the GUI window
        
        # Initialize recognition system
        print("Démarrage du système de reconnaissance...")
        self.system = FacialRecognitionSystem()
        self.system.load_dataset()
        if self.system.train_model():
            self.system.run_recognition()
        else:
            messagebox.showerror("Erreur", "Échec de l'entraînement du modèle")

def main():
    # Initialize database and process images if needed
    db = FaceDatabase()
    images_dir = "Images_visages"
    
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"Créé le dossier {images_dir}. Veuillez y ajouter des images de visages.")
        return

    # Process new images and add to database
    print("Mise à jour de la base de données...")
    db.process_directory(images_dir)

    # Start the GUI application
    app = FaceRecognitionApp()
    app.root.mainloop()

if __name__ == "__main__":
    main()