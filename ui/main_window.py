import customtkinter as ctk
from .components.main_container import MainContainer
import os

def get_theme_colors():
    """Récupère les couleurs du thème"""
    return {
        "light": {"bg": "#f8f9fa", "text": "#212529", "primary": "#4361ee"},
        "dark": {"bg": "#121212", "text": "#f8f9fa", "primary": "#4361ee"}
    }

def set_appearance_mode(mode):
    """Définit le mode d'apparence (light/dark)"""
    print(f"DEBUG: Définition du mode d'apparence: '{mode}'")
    ctk.set_appearance_mode(mode)

class MainWindow(ctk.CTk):
    """
    Fenêtre principale de l'application avec une barre latérale et un contenu dynamique.
    """
    
    def __init__(self, user_data=None):
        """
        Initialise la fenêtre principale.
        
        Args:
            user_data: Données de l'utilisateur connecté
        """
        super().__init__()
        print("DEBUG: Initialisation de MainWindow")
        
        # Configurer la fenêtre
        self.title("UGANC Stock - Gestion de stock")
        self.geometry("1280x720")
        self.minsize(1024, 600)
        
        # Enregistrer les données utilisateur
        self.user_data = user_data or {}
        print(f"DEBUG: Données utilisateur: {self.user_data}")
        
        # Configurer le thème
        set_appearance_mode("system")
        self.theme_colors = get_theme_colors()
        
        # Configurer la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Créer le conteneur principal
        self.main_container = MainContainer(self)
        self.main_container.pack(fill="both", expand=True)
        
        # Configurer le style de la fenêtre
        self._setup_window_style()
    
    def _setup_window_style(self):
        """Configure le style de la fenêtre"""
        print("DEBUG: Configuration du style de la fenêtre")
        # Définir l'icône si disponible
        try:
            icon_path = os.path.join("assets", "logo.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                print("DEBUG: Icône chargée")
            else:
                print("DEBUG: Icône non trouvée")
        except Exception as e:
            print(f"DEBUG: Erreur icône: {e}")
        
        # Configurer le thème
        ctk.set_default_color_theme("blue")
        
        # Configurer les polices
        ctk.CTkLabel._font = ("Segoe UI", 12)
        ctk.CTkButton._font = ("Segoe UI", 12, "bold")
        ctk.CTkEntry._font = ("Segoe UI", 12)
    
    def start(self):
        """Démarre l'application"""
        print("DEBUG: Démarrage de l'application")
        self.mainloop()


if __name__ == "__main__":
    app = MainWindow({
        "username": "admin",
        "full_name": "Administrateur",
        "role": "admin"
    })
    app.start()