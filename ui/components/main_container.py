import customtkinter as ctk
from typing import Dict, Optional
from .sidebar import Sidebar
import sys
import os

# Ajouter le répertoire racine au chemin Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class MainContainer(ctk.CTkFrame):
    """
    Conteneur principal qui gère la structure de l'application avec une barre latérale
    et un contenu dynamique qui change en fonction de la sélection.
    """
    
    def __init__(self, parent, **kwargs):
        """
        Initialise le conteneur principal.
        
        Args:
            parent: Le widget parent
            **kwargs: Arguments supplémentaires pour le CTkFrame
        """
        super().__init__(parent, **kwargs)
        print("DEBUG: Initialisation de MainContainer")
        
        # Configuration de la grille principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Dictionnaire pour stocker les frames de contenu
        self.content_frames: Dict[str, ctk.CTkFrame] = {}
        self.current_frame: Optional[ctk.CTkFrame] = None
        
        # Créer la barre latérale
        self.sidebar = Sidebar(self, on_button_click=self._on_sidebar_button_click)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Créer le conteneur pour le contenu principal
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(0, weight=1)
        
        # Créer les différents écrans de contenu
        self._create_content_frames()
        
        # Afficher le tableau de bord par défaut
        self.show_content("dashboard")
    
    def _create_content_frames(self):
        """Crée les différents écrans de contenu"""
        print("DEBUG: Création des frames de contenu")
        try:
            print("DEBUG: Tentative d'importation des écrans")
            from ui.screens.dashboard_screen import DashboardScreen
            from ui.screens.article_manager import ArticleManager
            from ui.screens.stock_manager import StockManager
            
            print("DEBUG: Importation réussie")
            
            # Frame du tableau de bord
            print("DEBUG: Création du dashboard")
            self.content_frames["dashboard"] = DashboardScreen(self.content_container)
            print("DEBUG: Dashboard créé")
            
            # Frame de gestion des articles
            print("DEBUG: Création des articles")
            self.content_frames["articles"] = ArticleManager(self.content_container)
            print("DEBUG: Articles créés")
            
            # Frame de gestion des stocks
            print("DEBUG: Création des stocks")
            self.content_frames["stock"] = StockManager(self.content_container)
            print("DEBUG: Stocks créés")
            
            # Frame des paramètres
            print("DEBUG: Création des paramètres")
            self.content_frames["parametres"] = ctk.CTkFrame(
                self.content_container, 
                fg_color="transparent"
            )
            ctk.CTkLabel(
                self.content_frames["parametres"],
                text="Paramètres (non implémenté)",
                font=("Segoe UI", 12)
            ).pack(expand=True)
            print("DEBUG: Paramètres créés")
            
            print(f"DEBUG: Frames créés: {list(self.content_frames.keys())}")
            
            # Masquer tous les frames
            for key, frame in self.content_frames.items():
                print(f"DEBUG: Masquage de '{key}'")
                frame.grid_forget()
            
        except ImportError as e:
            print(f"ERREUR: Importation échouée: {e}")
            print(f"DEBUG: Chemin Python: {sys.path}")
            print(f"DEBUG: Répertoire actuel: {os.getcwd()}")
            self.content_frames["error"] = ctk.CTkFrame(self.content_container, fg_color="transparent")
            ctk.CTkLabel(
                self.content_frames["error"],
                text=f"Erreur de chargement: {e}",
                text_color=("#dc3545", "#ff6b6b"),
                font=("Segoe UI", 12)
            ).pack(expand=True)
            self.content_frames["error"].grid_forget()
    
    def _on_sidebar_button_click(self, button_key: str):
        """
        Gère le clic sur un bouton de la barre latérale.
        
        Args:
            button_key: Clé du bouton cliqué (dashboard, articles, stock, parametres, etc.)
        """
        print(f"DEBUG: Clic reçu sur la clé: '{button_key}'")
        
        if button_key == "Déconnexion" or button_key == "deconnexion":
            print("DEBUG: Déconnexion")
            self.master.destroy()
            return
            
        self.show_content(button_key)
    
    def show_content(self, content_key: str):
        """
        Affiche le contenu correspondant à la clé spécifiée.
        
        Args:
            content_key: Clé du contenu à afficher
        """
        print(f"DEBUG: Affichage de '{content_key}'")
        print(f"DEBUG: Frames disponibles: {list(self.content_frames.keys())}")
        
        # Masquer le frame actuel s'il existe
        if self.current_frame:
            print(f"DEBUG: Masquage de {self.current_frame}")
            self.current_frame.grid_forget()
        
        # Vérifier si la clé existe
        if content_key not in self.content_frames:
            print(f"ERREUR: Clé '{content_key}' non trouvée")
            error_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
            ctk.CTkLabel(
                error_frame,
                text=f"Contenu non trouvé: {content_key}",
                text_color=("#dc3545", "#ff6b6b"),
                font=("Segoe UI", 12)
            ).pack(expand=True)
            self.current_frame = error_frame
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            return
        
        try:
            # Afficher le nouveau frame
            self.current_frame = self.content_frames[content_key]
            print(f"DEBUG: Affichage de {content_key}: {self.current_frame}")
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            self.current_frame.tkraise()
            
            # Mettre à jour le bouton actif dans la barre latérale
            if hasattr(self.sidebar, 'set_active_button'):
                print(f"DEBUG: Mise à jour du bouton actif: '{content_key}'")
                self.sidebar.set_active_button(content_key)
                
        except Exception as e:
            print(f"ERREUR: Affichage de '{content_key}' échoué: {e}")
            error_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
            ctk.CTkLabel(
                error_frame,
                text=f"Erreur: {e}",
                text_color=("#dc3545", "#ff6b6b"),
                font=("Segoe UI", 12)
            ).pack(expand=True)
            self.current_frame = error_frame
            self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def get_content_frame(self, frame_id: str) -> Optional[ctk.CTkFrame]:
        """Récupère le frame de contenu correspondant à l'identifiant."""
        print(f"DEBUG: Récupération du frame '{frame_id}'")
        return self.content_frames.get(frame_id)


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("UGANC Stock - Test")
    root.geometry("1200x700")
    container = MainContainer(root)
    container.pack(fill="both", expand=True)
    root.mainloop()