import tkinter as tk
from tkinter import ttk
from face_database_manager import FaceDatabase
import os
import sqlite3 
from tkinter import messagebox

class DatabaseViewer:
    def __init__(self, parent, app):  # Add app parameter
        self.parent = parent
        self.app = app  # Store reference to main app
        self.frame = tk.Frame(parent, bg='#f0f0f0')
        self.db = FaceDatabase()
        self.setup_gui()
        
    def go_back(self):
        self.frame.pack_forget()
        self.app.show_main_buttons()  # Use app reference instead of parent
    
    def show(self):
        self.frame.pack(fill='both', expand=True)
        
    def load_data(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Connect to database
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, image_path FROM face_encodings")
        
        # Check each image path
        for row in cursor.fetchall():
            image_path = row[2]
            if not os.path.exists(image_path):
                print(f"WARNING: Image not found: {image_path}")
            
            self.tree.insert('', 'end', values=row)
            
        conn.close()

    def setup_gui(self):
        # Create header frame
        header_frame = tk.Frame(self.frame, bg='#f0f0f0')
        header_frame.pack(fill='x', pady=10)
        
        # Back button
        back_button = tk.Button(
            header_frame,
            text="Retour",
            command=self.go_back,
            font=('Arial', 10),
            bg='#666666',
            fg='white',
            padx=10,
            pady=5
        )
        back_button.pack(side='left', padx=10)
        
        # Title
        tk.Label(
            header_frame,
            text="Base de données des visages",
            font=('Arial', 14, 'bold'),
            bg='#f0f0f0'
        ).pack(side='left', padx=10)
        
        # Add delete button
        delete_button = tk.Button(
            header_frame,
            text="Supprimer la sélection",
            command=self.delete_selected,
            font=('Arial', 10),
            bg='#dc3545',
            fg='white',
            padx=10,
            pady=5
        )
        delete_button.pack(side='right', padx=10)
        
        # Create treeview
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Nom', 'Chemin'), show='headings')
        
        # Configure columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nom', text='Nom')
        self.tree.heading('Chemin', text='Chemin de l\'image')
        
        self.tree.column('ID', width=50)
        self.tree.column('Nom', width=150)
        self.tree.column('Chemin', width=400)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Load data
        self.load_data()

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Attention", "Veuillez sélectionner une entrée à supprimer")
            return

        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ces entrées ?"):
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            for item in selected_items:
                values = self.tree.item(item)['values']
                entry_id = values[0]
                
                # Delete from database
                cursor.execute("DELETE FROM face_encodings WHERE id = ?", (entry_id,))
                
                # Remove from treeview
                self.tree.delete(item)
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Succès", "Entrées supprimées avec succès")