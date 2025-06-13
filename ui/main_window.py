"""
Fenêtre principale de l'application UGANC Stock.
"""
import customtkinter as ctk
from .components.main_container import MainContainer
from utils.theme_utils import setup_theme

def get_theme_colors():
    """Récupère les couleurs du thème"""
    return setup_theme()

def set_appearance_mode(mode):
    """Définit le mode d'apparence (light/dark)"""
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
        
        # Configurer la fenêtre
        self.title("UGANC Stock - Gestion de stock")
        self.geometry("1280x720")
        self.minsize(1024, 600)
        
        # Enregistrer les données utilisateur
        self.user_data = user_data or {}
        
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
        # Définir l'icône de la fenêtre si disponible
        try:
            self.iconbitmap("assets/logo.ico")
        except:
            pass
        
        # Configurer le thème de la fenêtre
        ctk.set_default_color_theme("blue")
        
        # Configurer le style des widgets
        ctk.CTkLabel._font = ("Segoe UI", 12)
        ctk.CTkButton._font = ("Segoe UI", 12, "bold")
        ctk.CTkEntry._font = ("Segoe UI", 12)
    
    def start(self):
        """Démarre l'application"""
        self.mainloop()


if __name__ == "__main__":
    # Exemple d'utilisation
    app = MainWindow({
        "username": "admin",
        "full_name": "Administrateur",
        "role": "admin"
    })
    app.start()
