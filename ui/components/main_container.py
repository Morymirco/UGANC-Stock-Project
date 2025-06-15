"""
Conteneur principal qui gère la structure de l'application avec une barre latérale et un contenu dynamique.
"""
import customtkinter as ctk
from typing import Dict, Optional
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
        self.show_content("dashboard")
    
    def _create_content_frames(self):
        """Crée les différents écrans de contenu"""
        print("Création des frames de contenu...")
        try:
            print("Tentative d'importation des écrans...")
            from ui.screens.dashboard_screen import DashboardScreen
            from ui.screens.article_manager import ArticleManager
            from ui.screens.stock_manager import StockManager
            
            print("Importation des écrans réussie")
            
            try:
                # Frame du tableau de bord
                print("Création du dashboard...")
                self.dashboard_frame = DashboardScreen(self.content_container)
                self.content_frames["dashboard"] = self.dashboard_frame
                print("Dashboard créé avec succès")
                
                # Frame de gestion des articles
                print("Création du gestionnaire d'articles...")
                self.articles_frame = ArticleManager(self.content_container)
                self.content_frames["articles"] = self.articles_frame
                print("Gestionnaire d'articles créé avec succès")
                
                # Frame de gestion des stocks
                print("Création du gestionnaire de stocks...")
                self.stock_frame = StockManager(self.content_container)
                self.content_frames["stock"] = self.stock_frame
                print("Gestionnaire de stocks créé avec succès")
                
                # Frame des paramètres (à implémenter)
                print("Création du cadre des paramètres...")
                self.settings_frame = ctk.CTkFrame(
                    self.content_container, 
                    fg_color="transparent"
                )
                self.content_frames["parametres"] = self.settings_frame
                print("Cadre des paramètres créé avec succès")
                
                # Afficher les clés des frames créés
                print(f"Frames créés: {list(self.content_frames.keys())}")
                
                # Masquer tous les frames sauf celui par défaut
                for key, frame in self.content_frames.items():
                    print(f"Masquage du frame: {key}")
                    frame.grid_forget()
                
                print("Tous les frames ont été masqués")
                
            except Exception as e:
                print(f"Erreur lors de la création des frames: {e}")
                raise
                
        except ImportError as e:
            import sys
            import os
            print(f"Erreur d'importation: {e}")
            print(f"Chemin Python: {sys.path}")
            print(f"Répertoire de travail: {os.getcwd()}")
            
            # Créer un cadre d'erreur si le chargement échoue
            error_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
            ctk.CTkLabel(
                error_frame,
                text=f"Erreur de chargement des écrans: {e}\nVeuillez vérifier les logs pour plus de détails.",
                text_color=("#dc3545", "#ff6b6b"),
                font=("Segoe UI", 12)
            ).pack(expand=True, padx=20, pady=20)
            self.content_frames["error"] = error_frame
    
    def _on_sidebar_button_click(self, button_name: str):
        """
        Gère le clic sur un bouton de la barre latérale.
        
        Args:
            button_name: Nom du bouton cliqué
        """
        print(f"\n=== Clic sur le bouton: {button_name} ===")
        
        # Mapper les noms des boutons aux identifiants de frame
        button_map = {
            "tableau de bord": "dashboard",
            "gestion des articles": "articles",
            "gestion des stocks": "stock",
            "paramètres": "parametres",
            "déconnexion": "logout"
        }
        
        key = button_name.lower()
        print(f"Clé du bouton: '{key}'")
        
        # Obtenir la clé du frame correspondant
        frame_key = button_map.get(key)
        
        if frame_key is None:
            print(f"ATTENTION: Aucune clé de frame trouvée pour le bouton: {button_name}")
            frame_key = "dashboard"  # Valeur par défaut
            
        print(f"Frame clé sélectionnée: {frame_key}")
        
        # Gérer la déconnexion
        if frame_key == "logout":
            print("Déconnexion demandée, fermeture de l'application...")
            self.master.destroy()  # Fermer la fenêtre principale
            return
            
        # Afficher le contenu correspondant
        print(f"Appel de show_content avec la clé: {frame_key}")
        self.show_content(frame_key)
    
    def show_content(self, content_key: str):
        """
        Affiche le contenu correspondant à la clé spécifiée.
        
        Args:
            content_key: Clé du contenu à afficher
        """
        print(f"\n=== Tentative d'affichage du contenu: {content_key} ===")
        print(f"Clés disponibles: {list(self.content_frames.keys())}")
        
        # Masquer le contenu actuel
        if self.current_frame:
            print(f"Masquage du frame actuel: {self.current_frame}")
            self.current_frame.grid_forget()
        
        # Vérifier si la clé existe
        if content_key not in self.content_frames:
            print(f"ERREUR: La clé '{content_key}' n'existe pas dans content_frames")
            # Afficher un message d'erreur
            error_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
            ctk.CTkLabel(
                error_frame,
                text=f"Contenu non trouvé: {content_key}\nClés disponibles: {', '.join(self.content_frames.keys())}",
                text_color=("#dc3545", "#ff6b6b"),
                font=("Segoe UI", 12)
            ).pack(expand=True, padx=20, pady=20)
            self.current_frame = error_frame
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            return
        
        try:
            # Récupérer et afficher le nouveau frame
            self.current_frame = self.content_frames[content_key]
            print(f"Affichage du frame: {content_key} (type: {type(self.current_frame)})")
            
            # Configurer la grille pour le nouveau frame
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            self.current_frame.tkraise()  # S'assurer que le frame est au premier plan
            
            # Mettre à jour la barre latérale
            if hasattr(self, 'sidebar') and hasattr(self.sidebar, 'set_active_button'):
                print(f"Mise à jour du bouton actif dans la barre latérale: {content_key}")
                self.sidebar.set_active_button(content_key)
            else:
                print("ATTENTION: Impossible de mettre à jour la barre latérale - sidebar ou set_active_button non disponible")
                
            print(f"=== Affichage de {content_key} réussi ===\n")
            
        except Exception as e:
            print(f"ERREUR lors de l'affichage de {content_key}: {e}")
            # Afficher un message d'erreur
            error_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
            ctk.CTkLabel(
                error_frame,
                text=f"Erreur lors de l'affichage de {content_key}: {str(e)}",
                text_color=("#dc3545", "#ff6b6b"),
                font=("Segoe UI", 12)
            ).pack(expand=True, padx=20, pady=20)
            self.current_frame = error_frame
            self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def get_content_frame(self, frame_id: str) -> Optional[ctk.CTkFrame]:
        """
        Récupère le frame de contenu correspondant à l'identifiant donné.
        
        Args:
            frame_id: Identifiant du frame à récupérer
            
        Returns:
            Le frame de contenu correspondant ou None si non trouvé
        """
        return self.content_frames.get(frame_id)


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
