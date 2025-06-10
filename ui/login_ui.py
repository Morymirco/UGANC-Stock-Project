"""
Module de l'interface de connexion du système de gestion de stock UGANC
"""
import os
import math
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageTk
import customtkinter as ctk

try:
    from core.auth_manager import AuthManager
    from ui.main_ui import MainUI
    from ui.components import ThemeToggle, LoginBanner, AutoCompleteEntry
    from utils.theme_utils import setup_theme
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    raise

class LoginUI:
    def __init__(self, root=None):
        """
        Initialise l'interface de connexion
        
        Args:
            root: Fenêtre racine (optionnel, en crée une nouvelle si None)
        """
        try:
            self.root = ctk.CTk() if root is None else root
            self.root.title("Système de Gestion de Stock - Connexion")
            
            # Configuration de la fenêtre
            self._setup_window()
            
            # Configuration du thème
            self.theme_colors = setup_theme()
            
            # Initialiser le gestionnaire d'authentification
            self.auth_manager = AuthManager()
            self._ensure_admin_exists()
            
            # Créer les widgets
            self._setup_ui()
            
            # Lancer la boucle principale si c'est la fenêtre racine
            if root is None:
                self.root.mainloop()
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de démarrer l'application: {str(e)}")
            if self.root:
                self.root.destroy()
            raise
    
    def _setup_window(self):
        """Configure la fenêtre principale"""
        window_width = 1000
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.resizable(False, False)
    
    def _ensure_admin_exists(self):
        """Vérifie et crée un compte admin si nécessaire"""
        success, message = self.auth_manager.create_admin_if_not_exists()
        if success:
            print(message)
    
    def _setup_ui(self):
        """Configure l'interface utilisateur"""
        # Frame principal avec deux colonnes
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Colonne de gauche - Formulaire de connexion
        self.left_frame = ctk.CTkFrame(self.main_frame, width=400, corner_radius=15)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.left_frame.pack_propagate(False)
        
        # Colonne de droite - Bannière
        self.banner = LoginBanner(self.main_frame, width=500, corner_radius=15)
        self.banner.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Contenu du formulaire de connexion
        self._setup_login_form()
        
        # Lier la touche Entrée au bouton de connexion
        self.root.bind("<Return>", lambda event: self.login())
    

    
    def _setup_login_form(self):
        """Configure le formulaire de connexion"""
        # Titre
        title = ctk.CTkLabel(
            self.left_frame,
            text="Connexion",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(60, 10))
        
        # Sous-titre
        subtitle = ctk.CTkLabel(
            self.left_frame,
            text="Accédez à votre espace personnel",
            text_color=("gray", "lightgray"),
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 40))
        
        # Frame pour les champs de saisie
        input_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        input_frame.pack(fill=tk.X, padx=40, pady=10)
        
        # Champ Nom d'utilisateur avec autocomplétion
        self.username_entry = AutoCompleteEntry(
            input_frame,
            placeholder="Nom d'utilisateur",
            get_suggestions=self._get_username_suggestions
        )
        self.username_entry.pack(fill=tk.X, pady=5)
        self.username_entry.on_select = self._on_username_selected
        
        # Champ Mot de passe
        self.password_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Mot de passe",
            height=45,
            corner_radius=10,
            show="•",
            font=("Arial", 14)
        )
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Case à cocher "Se souvenir de moi"
        self.remember_me = ctk.CTkCheckBox(
            input_frame,
            text="Se souvenir de moi",
            font=("Arial", 12)
        )
        self.remember_me.pack(pady=(10, 0), anchor="w")
        
        # Bouton de connexion
        login_button = ctk.CTkButton(
            input_frame,
            text="Se connecter",
            height=45,
            corner_radius=10,
            font=("Arial", 14, "bold"),
            command=self.login
        )
        login_button.pack(fill=tk.X, pady=(30, 10))
        
        # Lien "Mot de passe oublié ?"
        forgot_password = ctk.CTkButton(
            input_frame,
            text="Mot de passe oublié ?",
            fg_color="transparent",
            text_color=("gray", "lightgray"),
            hover=False,
            font=("Arial", 12, "underline"),
            command=self.forgot_password
        )
        forgot_password.pack(pady=5)
        
        # Pied de page
        self._setup_footer()
    
    def _setup_footer(self):
        """Configure le pied de page avec le sélecteur de thème et la version"""
        # Frame pour le bas de la fenêtre
        bottom_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 20), padx=20)
        
        # Bouton de basculement de thème
        self.theme_toggle = ThemeToggle(bottom_frame)
        self.theme_toggle.pack(side=tk.RIGHT, padx=5)
        
        # Version de l'application
        version = ctk.CTkLabel(
            bottom_frame,
            text="Version 1.0.0",
            text_color=("gray", "lightgray"),
            font=("Arial", 10)
        )
        version.pack(side=tk.LEFT, pady=5)
    
    def _get_username_suggestions(self, text: str) -> list:
        """Récupère les suggestions de noms d'utilisateur"""
        try:
            with self.auth_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT username FROM Utilisateurs WHERE username LIKE ?",
                    (f"%{text}%",)
                )
                return [row[0] for row in cursor.fetchall()]
        except Exception as e:
            print(f"Erreur lors de la récupération des suggestions : {e}")
            return []
    
    def _on_username_selected(self, username: str):
        """Appelé lorsqu'un nom d'utilisateur est sélectionné"""
        self.password_entry.focus()
    
    def login(self, event=None):
        """
        Gère la tentative de connexion
        
        Args:
            event: Événement de déclenchement (pour la touche Entrée)
        """
        try:
            username = self.username_entry.get().strip()
            password = self.password_entry.get()
            
            if not username or not password:
                messagebox.showerror("Erreur", "Veuillez saisir un nom d'utilisateur et un mot de passe", parent=self.root)
                return
            
            # Afficher un indicateur de chargement
            loading = ctk.CTkLabel(
                self.left_frame,
                text="Connexion en cours...",
                text_color=("gray", "lightgray"),
                font=("Arial", 12)
            )
            loading.pack(pady=10)
            self.root.update()
            
            try:
                # Vérifier les identifiants
                success, message = self.auth_manager.login(username, password)
                
                if success:
                    # Fermer la fenêtre de connexion
                    self.root.withdraw()
                    
                    # Récupérer les informations de l'utilisateur connecté
                    user = self.auth_manager.get_current_user()
                    
                    # Ouvrir la fenêtre principale
                    self.open_main_app(user)
                else:
                    messagebox.showerror(
                        "Erreur", 
                        "Nom d'utilisateur ou mot de passe incorrect",
                        parent=self.root
                    )
            except Exception as e:
                messagebox.showerror(
                    "Erreur", 
                    f"Une erreur est survenue lors de l'authentification: {str(e)}",
                    parent=self.root
                )
            finally:
                # Masquer l'indicateur de chargement
                loading.destroy()
                
        except Exception as e:
            messagebox.showerror(
                "Erreur", 
                f"Une erreur inattendue est survenue: {str(e)}",
                parent=self.root
            )
    
    def forgot_password(self):
        """Affiche une boîte de dialogue pour la réinitialisation du mot de passe"""
        dialog = ctk.CTkInputDialog(
            text="Entrez votre nom d'utilisateur pour réinitialiser votre mot de passe :",
            title="Réinitialisation du mot de passe"
        )
        username = dialog.get_input()
        
        if username:
            # Ici, vous pourriez implémenter la logique de réinitialisation
            messagebox.showinfo("Information", f"Un email de réinitialisation a été envoyé à l'adresse associée à {username}")
    
    def create_theme_icon(self):
        """Crée une icône de thème dynamique"""
        size = 20
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        if ctk.get_appearance_mode() == "Dark":
            # Icône de lune pour le mode sombre
            draw.ellipse((0, 0, size-1, size-1), fill="#f0f0f0")
            draw.ellipse((size//3, 0, size-1, size*2//3), fill="#1a1a1a")
        else:
            # Icône de soleil pour le mode clair
            draw.ellipse((0, 0, size-1, size-1), fill="#ffd700")
            # Rayons du soleil
            for i in range(8):
                angle = i * 45
                x1 = size//2 + int((size//2 - 2) * 0.7 * math.cos(math.radians(angle)))
                y1 = size//2 + int((size//2 - 2) * 0.7 * math.sin(math.radians(angle)))
                x2 = size//2 + int((size//2 + 2) * 1.5 * math.cos(math.radians(angle)))
                y2 = size//2 + int((size//2 + 2) * 1.5 * math.sin(math.radians(angle)))
                draw.line([(x1, y1), (x2, y2)], fill="#ffd700", width=2)
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    
    def toggle_theme(self):
        """Bascule entre les thèmes clair et sombre"""
        current_theme = ctk.get_appearance_mode().lower()
        new_theme = "dark" if current_theme == "light" else "light"
        ctk.set_appearance_mode(new_theme)
        
        # Mettre à jour l'icône du bouton
        self.theme_icon = self.create_theme_icon()
        self.theme_button.configure(image=self.theme_icon)
        
        # Mettre à jour les couleurs des éléments personnalisés
        self.update_theme_colors()
    
    def update_theme_colors(self):
        """Met à jour les couleurs en fonction du thème actuel"""
        current_theme = ctk.get_appearance_mode().lower()
        colors = self.theme_colors[current_theme]
        
        # Mettre à jour les couleurs des éléments personnalisés si nécessaire
        self.left_frame.configure(fg_color=colors["frame_bg"])
        
    def on_theme_change(self, theme):
        """Appelé lorsque le thème du système change"""
        if theme.lower() != ctk.get_appearance_mode().lower():
            ctk.set_appearance_mode(theme)
            self.update_theme_colors()
    
    def open_main_app(self, user):
        """
        Ouvre l'application principale après une connexion réussie
        
        Args:
            user: Dictionnaire contenant les informations de l'utilisateur connecté
        """
        try:
            self.root.withdraw()  # Cacher la fenêtre de connexion
            
            # Créer une nouvelle fenêtre pour l'application principale
            main_window = ctk.CTkToplevel(self.root)
            main_window.title("Système de Gestion de Stock")
            main_window.geometry("1280x720")  # Taille par défaut plus grande
            
            # Positionner la fenêtre au centre
            window_width = 1280
            window_height = 720
            screen_width = main_window.winfo_screenwidth()
            screen_height = main_window.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
            
            # Définir le comportement de fermeture
            main_window.protocol("WM_DELETE_WINDOW", self.on_main_close)
            
            # Initialiser l'interface principale avec l'auth_manager
            self.main_app = MainUI(main_window, self.auth_manager)
            
            # Configurer la fenêtre principale
            main_window.focus_force()
            
        except Exception as e:
            messagebox.showerror(
                "Erreur", 
                f"Impossible d'ouvrir l'application principale: {str(e)}",
                parent=self.root
            )
            self.root.deiconify()  # Réafficher la fenêtre de connexion en cas d'erreur
    
    def on_main_close(self):
        """
        Gère la fermeture de l'application principale
        
        Demande une confirmation avant de fermer l'application
        """
        if messagebox.askyesno(
            "Quitter", 
            "Êtes-vous sûr de vouloir quitter l'application ?",
            parent=self.root
        ):
            try:
                if hasattr(self, 'main_app') and hasattr(self.main_app, 'cleanup'):
                    self.main_app.cleanup()
            except Exception as e:
                print(f"Erreur lors du nettoyage: {e}")
            finally:
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


