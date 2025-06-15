import customtkinter as ctk
from typing import Dict, Callable, Optional

class Sidebar(ctk.CTkFrame):
    """
Barre latérale moderne et personnalisable pour l'application de gestion de stock.
Utilise CustomTkinter pour un rendu moderne et une meilleure expérience utilisateur.
"""
    
    def __init__(self, parent, on_button_click: Callable[[str], None] = None, **kwargs):
        """
        Initialise la barre latérale avec un design moderne.
        
        Args:
            parent: Le widget parent
            on_button_click: Fonction de rappel appelée lorsqu'un bouton est cliqué
            **kwargs: Arguments supplémentaires pour le CTkFrame
        """
        super().__init__(parent, **kwargs)
        self.on_button_click = on_button_click
        self.buttons: Dict[str, ctk.CTkButton] = {}
        self.active_button: Optional[str] = None
        
        # Récupérer les couleurs du thème
        self.theme_colors = {
            "light": {
                "bg": "#f8f9fa",
                "sidebar_bg": "#ffffff",
                "hover": "#e9ecef",
                "active": "#e0f7fa",
                "text": "#212529",
                "primary": "#4361ee"
            },
            "dark": {
                "bg": "#121212",
                "sidebar_bg": "#1e1e1e",
                "hover": "#2d2d2d",
                "active": "#1e3a5f",
                "text": "#f8f9fa",
                "primary": "#4361ee"
            }
        }
        
        # Configuration du style
        self.configure(
            fg_color=(self.theme_colors["light"]["sidebar_bg"], 
                     self.theme_colors["dark"]["sidebar_bg"]),
            corner_radius=0
        )
        
        # Création des widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Crée et positionne les widgets de la barre latérale avec un design moderne"""
        # Configuration de la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Ligne principale pour le contenu
        
        # En-tête avec logo
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 5))
        
        # Logo et nom de l'application
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="📊",
            font=("Arial", 24),
            text_color=(self.theme_colors["light"]["primary"], 
                       self.theme_colors["dark"]["primary"])
        )
        self.logo_label.pack(side="left", padx=(0, 10))
        
        self.app_name = ctk.CTkLabel(
            self.header_frame,
            text="UGANC Stock",
            font=("Arial", 18, "bold"),
            text_color=(self.theme_colors["light"]["text"], 
                       self.theme_colors["dark"]["text"])
        )
        self.app_name.pack(side="left")
        
        # Cadre pour les boutons de navigation
        self.buttons_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        
        # Liste des boutons de navigation
        menu_items = [
            ("Tableau de bord", "📊", "dashboard"),
            ("Gestion des articles", "📝", "articles"),
            ("Gestion des stocks", "📦", "stock"),
            ("Paramètres", "⚙️", "parametres")
        ]
        
        # Création des boutons de navigation
        for i, (text, icon, key) in enumerate(menu_items):
            # Cadre pour le bouton et l'indicateur
            btn_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent", height=50)
            btn_frame.grid(row=i, column=0, sticky="ew", pady=2)
            btn_frame.grid_columnconfigure(1, weight=1)
            
            # Indicateur de sélection
            indicator = ctk.CTkLabel(
                btn_frame, 
                text="", 
                width=4,
                corner_radius=2,
                fg_color="transparent"
            )
            indicator.grid(row=0, column=0, sticky="ns", padx=5)
            
            # Bouton de navigation
            btn = ctk.CTkButton(
                btn_frame,
                text=f"  {icon}  {text}",
                font=("Segoe UI", 14),
                anchor="w",
                fg_color="transparent",
                text_color=(self.theme_colors["light"]["text"], 
                           self.theme_colors["dark"]["text"]),
                hover_color=(self.theme_colors["light"]["hover"], 
                            self.theme_colors["dark"]["hover"]),
                corner_radius=8,
                height=45,
                command=lambda t=text: self._on_button_click(t)
            )
            btn.grid(row=0, column=1, sticky="ew", padx=(0, 5))
            
            # Stocker les références
            self.buttons[key] = {
                'button': btn,
                'indicator': indicator,
                'frame': btn_frame
            }
            
            # Événements de survol
            btn.bind("<Enter>", lambda e, k=key: self._on_hover(k, True))
            btn.bind("<Leave>", lambda e, k=key: self._on_hover(k, False))
        
        # Espacement
        self.buttons_frame.rowconfigure(len(menu_items), weight=1)
        
        # Pied de page avec bouton de déconnexion
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.footer_frame.grid(row=2, column=0, sticky="sew", padx=10, pady=(0, 15))
        
        # Bouton de déconnexion
        self.logout_btn = ctk.CTkButton(
            self.footer_frame,
            text="Déconnexion",
            font=("Segoe UI", 13, "bold"),
            fg_color="transparent",
            border_width=2,
            border_color=("#dc3545", "#ff6b6b"),
            text_color=("#dc3545", "#ff6b6b"),
            hover_color=("#f8d7da", "#84202920"),
            corner_radius=8,
            height=45,
            anchor="center",
            command=lambda: self._on_button_click("déconnexion")
        )
        self.logout_btn.pack(fill="x", pady=(5, 0))
    
    def _on_button_click(self, button_name: str):
        """
        Gère le clic sur un bouton de la barre latérale avec animation.
        
        Args:
            button_name: Nom du bouton cliqué
        """
        # Convertir le nom du bouton en clé
        key = button_name.lower()
        
        # Mettre à jour le style du bouton actif
        self.set_active_button(key)
        
        # Animer l'indicateur de sélection
        if key in self.buttons:
            self._animate_indicator(key)
        
        # Appeler la fonction de rappel
        if self.on_button_click:
            self.on_button_click(button_name)
    
    def _on_hover(self, button_key: str, is_hovered: bool):
        """
        Gère l'effet de survol sur les boutons.
        
        Args:
            button_key: Clé du bouton survolé
            is_hovered: Si le bouton est survolé
        """
        if button_key in self.buttons:
            btn = self.buttons[button_key]['button']
            indicator = self.buttons[button_key]['indicator']
            
            if is_hovered:
                # Effet de survol
                btn.configure(
                    fg_color=(self.theme_colors["light"]["hover"], 
                             self.theme_colors["dark"]["hover"])
                )
                indicator.configure(
                    fg_color=(self.theme_colors["light"]["primary"], 
                             self.theme_colors["dark"]["primary"])
                )
            else:
                # Réinitialiser si ce n'est pas le bouton actif
                if button_key != self.active_button:
                    btn.configure(fg_color="transparent")
                    indicator.configure(fg_color="transparent")
    
    def _animate_indicator(self, button_key: str):
        """
        Anime l'indicateur de sélection vers le bouton cliqué.
        
        Args:
            button_key: Clé du bouton sélectionné
        """
        if button_key in self.buttons:
            # Réinitialiser tous les indicateurs
            for key, elements in self.buttons.items():
                elements['indicator'].configure(fg_color="transparent")
                elements['button'].configure(
                    font=("Segoe UI", 14),
                    text_color=(self.theme_colors["light"]["text"], 
                               self.theme_colors["dark"]["text"])
                )
            
            # Mettre en surbrillance le bouton actif
            self.buttons[button_key]['indicator'].configure(
                fg_color=(self.theme_colors["light"]["primary"], 
                         self.theme_colors["dark"]["primary"])
            )
            self.buttons[button_key]['button'].configure(
                font=("Segoe UI", 14, "bold"),
                text_color=(self.theme_colors["light"]["primary"], 
                           self.theme_colors["dark"]["primary"])
            )
            
            # Faire défiler jusqu'au bouton si nécessaire
            self.buttons_frame._parent_canvas.yview_moveto(0)
    
    def set_active_button(self, button_name: str):
        """
        Définit le bouton actif et met à jour l'interface.
        
        Args:
            button_name: Nom ou clé du bouton à définir comme actif
        """
        # Convertir le nom du bouton en clé si nécessaire
        button_key = button_name.lower()
        
        # Mettre à jour le bouton actif
        self.active_button = button_key
        self._animate_indicator(button_key)
        
        # Mettre à jour les couleurs de survol
        for key, elements in self.buttons.items():
            if key != button_key:
                elements['button'].configure(
                    fg_color="transparent",
                    hover_color=(self.theme_colors["light"]["hover"], 
                                self.theme_colors["dark"]["hover"]),
                    text_color=(self.theme_colors["light"]["text"], 
                               self.theme_colors["dark"]["text"]),
                    font=("Segoe UI", 14)
                )
            else:
                elements['button'].configure(
                    fg_color=(self.theme_colors["light"]["active"], 
                             self.theme_colors["dark"]["active"]),
                    hover_color=(self.theme_colors["light"]["active"], 
                                self.theme_colors["dark"]["active"]),
                    text_color=(self.theme_colors["light"]["primary"], 
                               self.theme_colors["dark"]["primary"]),
                    font=("Segoe UI", 14, "bold")
                )
    
    def get_active_button(self) -> Optional[str]:
        """
        Retourne le nom du bouton actuellement sélectionné.
        
        Returns:
            str: Nom du bouton actif ou None si aucun bouton n'est sélectionné
        """
        return self.active_button
    
    def set_width(self, width: int):
        """
        Définit la largeur de la barre latérale.
        
        Args:
            width: Largeur en pixels
        """
        self.configure(width=width)
        self.buttons_frame.configure(width=width - 10)
    
    def set_theme(self, theme: str):
        """
        Change le thème de la barre latérale (clair/sombre).
        
        Args:
            theme: 'light' pour le thème clair, 'dark' pour le thème sombre
        """
        if theme.lower() == "dark":
            # Thème sombre
            self.configure(fg_color="#1a2a44")
            self.buttons_frame.configure(fg_color="#1a2a44")
            self.separator.configure(fg_color="#4a5a7a")
            
            # Mise à jour des couleurs des boutons pour le thème sombre
            for btn in self.buttons.values():
                btn.configure(
                    text_color="#e6e9ef",
                    hover_color="#2a3d66",
                    fg_color="transparent"
                )
            self.logout_btn.configure(
                text_color="#ff6b6b",
                hover_color="#842029",
                fg_color="transparent"
            )
        else:
            # Thème clair
            self.configure(fg_color="#e6f0fa")
            self.buttons_frame.configure(fg_color="#e6f0fa")
            self.separator.configure(fg_color="#b3c7e6")
            
            # Mise à jour des couleurs des boutons pour le thème clair
            for btn in self.buttons.values():
                btn.configure(
                    text_color="#1a1e21",
                    hover_color="#d1e0f0",
                    fg_color="transparent"
                )
            self.logout_btn.configure(
                text_color="#dc3545",
                hover_color="#f8d7da",
                fg_color="transparent"
            )
        
        # Si un bouton est actif, on le remet en surbrillance avec les nouvelles couleurs
        if self.active_button and self.active_button in self.buttons:
            self.set_active_button(self.active_button)