import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import face_recognition
from face_database_manager import FaceDatabase

class ImageManagerWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Ajouter un visage")
        self.window.geometry("400x200")
        self.window.configure(bg='#f0f0f0')
        
        self.db = FaceDatabase()
        self.setup_gui()
        
    def setup_gui(self):
        # Name input
        name_frame = tk.Frame(self.window, bg='#f0f0f0')
        name_frame.pack(pady=20)
        
        tk.Label(name_frame, text="Nom:", bg='#f0f0f0', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(name_frame, font=('Arial', 10))
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        # Image selection button
        select_button = tk.Button(
            self.window,
            text="Sélectionner une image",
            command=self.process_image,
            font=('Arial', 10),
            bg='#4CAF50',
            fg='white',
            padx=15,
            pady=5
        )
        select_button.pack(pady=10)
        
    def process_image(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Erreur", "Veuillez entrer un nom")
            return
            
        # Select image file
        image_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.jpeg *.png")]
        )
        if not image_path:
            return
            
        # Create person directory
        person_dir = os.path.join("Images_visages", name)
        os.makedirs(person_dir, exist_ok=True)
        
        try:
            # Check if image contains a face
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            
            if not face_locations:
                # No face found - clean up and show error
                shutil.rmtree(person_dir)
                messagebox.showerror("Erreur", "Aucun visage détecté dans l'image")
                return
                
            # Copy image to person directory
            new_path = os.path.join(person_dir, os.path.basename(image_path))
            shutil.copy2(image_path, new_path)
            
            # Update database
            self.db.process_directory("Images_visages")
            
            messagebox.showinfo("Succès", "Image ajoutée avec succès")
            self.window.destroy()
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(person_dir):
                shutil.rmtree(person_dir)
            messagebox.showerror("Erreur", f"Erreur lors du traitement: {str(e)}")