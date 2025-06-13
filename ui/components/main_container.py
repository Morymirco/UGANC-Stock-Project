"""
Conteneur principal qui gère la structure de l'application avec une barre latérale et un contenu dynamique.
"""
import customtkinter as ctk
from typing import Dict, Type, Any, Optional
from .sidebar import Sidebar

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
        self.show_content("accueil")
    
    def _create_content_frames(self):
        """Crée les différents écrans de contenu"""
        # Frame d'accueil
        self._create_content_frame("accueil", "Tableau de bord")
        
        # Frame de gestion des stocks
        self._create_content_frame("stock", "Gestion des stocks")
        
        # Frame des ventes
        self._create_content_frame("ventes", "Gestion des ventes")
        
        # Frame des rapports
        self._create_content_frame("rapports", "Rapports et statistiques")
        
        # Frame des paramètres
        self._create_content_frame("parametres", "Paramètres de l'application")
    
    def _create_content_frame(self, frame_id: str, title: str):
        """
        Crée un nouveau frame de contenu.
        
        Args:
            frame_id: Identifiant unique du frame
            title: Titre à afficher dans le frame
        """
        # Créer le frame avec une bordure et un fond
        frame = ctk.CTkFrame(
            self.content_container,
            corner_radius=10,
            fg_color=("#ffffff", "#1e1e1e"),
            border_width=1,
            border_color=("#e0e0e0", "#333333")
        )
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        # Ajouter un en-tête
        header = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 18, "bold"),
            padx=20,
            pady=15,
            anchor="w"
        )
        header.grid(row=0, column=0, sticky="ew")
        
        # Ajouter un séparateur
        separator = ctk.CTkFrame(frame, height=1, fg_color=("#e0e0e0", "#333333"))
        separator.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Zone de contenu principale
        content = ctk.CTkFrame(frame, fg_color="transparent")
        content.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        content.grid_columnconfigure(0, weight=1)
        
        # Stocker le frame de contenu pour une utilisation ultérieure
        self.content_frames[frame_id] = content
        
        # Masquer le frame par défaut
        frame.grid_remove()
    
    def _on_sidebar_button_click(self, button_name: str):
        """
        Gère le clic sur un bouton de la barre latérale.
        
        Args:
            button_name: Nom du bouton cliqué
        """
        # Mapper les noms des boutons aux identifiants de frame
        button_mapping = {
            "accueil": "accueil",
            "tableau de bord": "accueil",
            "gestion des stocks": "stock",
            "stocks": "stock",
            "ventes": "ventes",
            "rapports": "rapports",
            "paramètres": "parametres",
            "parametres": "parametres",
            "déconnexion": "deconnexion"
        }
        
        # Convertir en minuscules pour la correspondance
        button_name = button_name.lower()
        
        # Vérifier si c'est la déconnexion
        if button_name == "déconnexion":
            self.master.destroy()  # Fermer l'application
            return
        
        # Afficher le contenu correspondant
        frame_id = button_mapping.get(button_name, "accueil")
        self.show_content(frame_id)
    
    def show_content(self, frame_id: str):
        """
        Affiche le contenu correspondant à l'identifiant donné.
        
        Args:
            frame_id: Identifiant du frame à afficher
        """
        # Masquer le frame actuel s'il y en a un
        if self.current_frame:
            self.current_frame.grid_remove()
        
        # Afficher le nouveau frame
        if frame_id in self.content_frames:
            self.current_frame = self.content_frames[frame_id].master
            self.current_frame.grid()
            
            # Mettre à jour la barre latérale
            self.sidebar.set_active_button(frame_id)
    
    def get_content_frame(self, frame_id: str) -> ctk.CTkFrame:
        """
        Récupère le frame de contenu correspondant à l'identifiant donné.
        
        Args:
            frame_id: Identifiant du frame à récupérer
            
        Returns:
            Le frame de contenu correspondant
        """
        return self.content_frames.get(frame_id, None)


if __name__ == "__main__":
    # Exemple d'utilisation
    root = ctk.CTk()
    root.title("UGANC Stock - Gestion de stock")
    root.geometry("1200x700")
    
    # Créer le conteneur principal
    container = MainContainer(root)
    container.pack(fill="both", expand=True)
    
    # Démarrer la boucle principale
    root.mainloop()
