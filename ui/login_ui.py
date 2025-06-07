# ui/login_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from core.auth_manager import AuthManager
from ui.main_ui import MainUI

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion de Stock - Connexion")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Centrer la fenêtre
        self.center_window()
        
        # Initialiser le gestionnaire d'authentification
        self.auth_manager = AuthManager()
        
        # S'assurer qu'un compte admin existe
        success, message = self.auth_manager.create_admin_if_not_exists()
        if success:
            print(message)
        
        # Créer les widgets
        self.create_widgets()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Crée les widgets de l'interface de connexion"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Connexion au Système", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les champs de saisie
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Nom d'utilisateur
        username_label = ttk.Label(input_frame, text="Nom d'utilisateur:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.username_entry = ttk.Entry(input_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)
        
        # Mot de passe
        password_label = ttk.Label(input_frame, text="Mot de passe:")
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.password_entry = ttk.Entry(input_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        
        # Bouton de connexion
        login_button = ttk.Button(main_frame, text="Se connecter", command=self.login)
        login_button.pack(pady=10)
        
        # Bouton pour créer un nouvel utilisateur (visible uniquement pour les admins)
        self.register_button = ttk.Button(main_frame, text="Créer un utilisateur", command=self.show_register_window)
        self.register_button.pack(pady=5)
        self.register_button.pack_forget()  # Caché par défaut
        
        # Lier la touche Entrée au bouton de connexion
        self.root.bind("<Return>", lambda event: self.login())
    
    def login(self):
        """Gère la tentative de connexion"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        success, message = self.auth_manager.login(username, password)
        if success:
            messagebox.showinfo("Succès", message)
            self.open_main_app()
        else:
            messagebox.showerror("Erreur", message)
    
    def open_main_app(self):
        """Ouvre l'application principale après connexion réussie"""
        self.root.withdraw()  # Cacher la fenêtre de connexion
        
        # Créer une nouvelle fenêtre pour l'application principale
        main_window = tk.Toplevel(self.root)
        main_window.title("Système de Gestion de Stock")
        main_window.geometry("800x600")
        main_window.protocol("WM_DELETE_WINDOW", self.on_main_close)
        
        # Initialiser l'interface principale
        MainUI(main_window, self.auth_manager)
    
    def on_main_close(self):
        """Gère la fermeture de l'application principale"""
        self.root.destroy()  # Fermer complètement l'application
    
    def show_register_window(self):
        """Affiche la fenêtre d'enregistrement d'un nouvel utilisateur"""
        register_window = tk.Toplevel(self.root)
        register_window.title("Créer un nouvel utilisateur")
        register_window.geometry("400x350")
        register_window.resizable(False, False)
        register_window.transient(self.root)  # Fenêtre modale
        register_window.grab_set()  # Empêche l'interaction avec la fenêtre parente
        
        # Centrer la fenêtre
        register_window.update_idletasks()
        width = register_window.winfo_width()
        height = register_window.winfo_height()
        x = (register_window.winfo_screenwidth() // 2) - (width // 2)
        y = (register_window.winfo_screenheight() // 2) - (height // 2)
        register_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(register_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Créer un nouvel utilisateur", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les champs de saisie
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Nom d'utilisateur
        username_label = ttk.Label(input_frame, text="Nom d'utilisateur:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        username_entry = ttk.Entry(input_frame, width=30)
        username_entry.grid(row=0, column=1, pady=5)
        
        # Mot de passe
        password_label = ttk.Label(input_frame, text="Mot de passe:")
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        password_entry = ttk.Entry(input_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        # Nom complet
        fullname_label = ttk.Label(input_frame, text="Nom complet:")
        fullname_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        fullname_entry = ttk.Entry(input_frame, width=30)
        fullname_entry.grid(row=2, column=1, pady=5)
        
        # Rôle
        role_label = ttk.Label(input_frame, text="Rôle:")
        role_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        role_combobox = ttk.Combobox(input_frame, width=28, state="readonly")
        role_combobox["values"] = ["admin", "gestionnaire", "vendeur"]
        role_combobox.current(1)  # Sélectionner "gestionnaire" par défaut
        role_combobox.grid(row=3, column=1, pady=5)
        
        # Frame pour les boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Fonction pour enregistrer l'utilisateur
        def register():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            role = role_combobox.get()
            
            if not username or not password or not fullname:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs", parent=register_window)
                return
            
            success, message = self.auth_manager.register_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Succès", message, parent=register_window)
                register_window.destroy()
            else:
                messagebox.showerror("Erreur", message, parent=register_window)
        
        # Boutons
        register_button = ttk.Button(button_frame, text="Enregistrer", command=register)
        register_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="Annuler", command=register_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)


