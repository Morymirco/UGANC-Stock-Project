"""
Bannière latérale pour l'écran de connexion
"""
import os
import urllib.request
import customtkinter as ctk
from PIL import Image

class LoginBanner(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=("#2b579a", "#1a3d7a"))
        
        # Charger l'image de fond
        self._load_background_image()
    
    def _load_background_image(self):
        """Charge et affiche l'image de fond"""
        try:
            # Essayer de charger une image locale
            image_path = os.path.join("ui", "assets", "login_bg.jpg")
            if not os.path.exists(image_path):
                # Créer le répertoire assets s'il n'existe pas
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                # Télécharger une image par défaut si elle n'existe pas
                self._download_default_image(image_path)
            
            # Charger et redimensionner l'image
            original_image = Image.open(image_path)
            resized_image = original_image.resize((500, 560), Image.LANCZOS)
            
            # Convertir en format compatible avec CTk
            self.bg_image = ctk.CTkImage(light_image=resized_image, size=(500, 560))
            
            # Afficher l'image
            bg_label = ctk.CTkLabel(
                self, 
                image=self.bg_image,
                text=""  # Pas de texte
            )
            bg_label.pack(fill=ctk.BOTH, expand=True)
            
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")
            self._show_fallback_ui()
    
    def _download_default_image(self, save_path):
        """Télécharge une image par défaut si aucune n'est trouvée"""
        try:
            # URL d'une image de fond par défaut
            default_image_url = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
            urllib.request.urlretrieve(default_image_url, save_path)
        except Exception as e:
            print(f"Impossible de télécharger l'image par défaut : {e}")
    
    def _show_fallback_ui(self):
        """Affiche une interface de secours si le chargement de l'image échoue"""
        # Ajouter un texte à la place de l'image
        title = ctk.CTkLabel(
            self,
            text="UGANC Stock",
            font=("Arial", 32, "bold"),
            text_color="white"
        )
        title.pack(pady=100)
        
        subtitle = ctk.CTkLabel(
            self,
            text="Système de Gestion de Stock",
            font=("Arial", 16),
            text_color="white"
        )
        subtitle.pack()
