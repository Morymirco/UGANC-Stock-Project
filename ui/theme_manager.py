import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """Gestionnaire de thèmes pour l'application"""
    
    def __init__(self):
        self.current_theme = "dark"  # "light" ou "dark"
        self.themes = {
            "dark": {
                "bg_primary": "#2c3e50",
                "bg_secondary": "#34495e", 
                "bg_tertiary": "#1a252f",
                "bg_card": "#34495e",
                "bg_input": "#95a5a6",
                "fg_primary": "#ecf0f1",
                "fg_secondary": "#bdc3c7",
                "fg_tertiary": "#7f8c8d",
                "accent_success": "#27ae60",
                "accent_danger": "#e74c3c",
                "accent_warning": "#f39c12",
                "accent_info": "#3498db",
                "accent_primary": "#9b59b6",
                "border": "#7f8c8d",
                "separator": "#7f8c8d"
            },
            "light": {
                "bg_primary": "#f8f9fa",
                "bg_secondary": "#ffffff",
                "bg_tertiary": "#343a40",
                "bg_card": "#ffffff",
                "bg_input": "#f8f9fa",
                "fg_primary": "#212529",
                "fg_secondary": "#495057",
                "fg_tertiary": "#6c757d",
                "accent_success": "#28a745",
                "accent_danger": "#dc3545",
                "accent_warning": "#ffc107",
                "accent_info": "#17a2b8",
                "accent_primary": "#007bff",
                "border": "#dee2e6",
                "separator": "#dee2e6"
            }
        }
    
    def get_color(self, color_name):
        """Retourne la couleur selon le thème actuel"""
        return self.themes[self.current_theme].get(color_name, "#000000")
    
    def toggle_theme(self):
        """Bascule entre les thèmes light et dark"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
    
    def apply_theme_to_window(self, window):
        """Applique le thème à une fenêtre"""
        window.configure(bg=self.get_color("bg_primary"))
    
    def get_button_style(self, style_type="primary"):
        """Retourne le style de bouton selon le type"""
        styles = {
            "primary": {
                "bg": self.get_color("accent_primary"),
                "fg": "#ffffff",
                "borderwidth": 0,
                "cursor": "hand2"
            },
            "success": {
                "bg": self.get_color("accent_success"),
                "fg": "#ffffff", 
                "borderwidth": 0,
                "cursor": "hand2"
            },
            "danger": {
                "bg": self.get_color("accent_danger"),
                "fg": "#ffffff",
                "borderwidth": 0,
                "cursor": "hand2"
            },
            "secondary": {
                "bg": self.get_color("bg_tertiary"),
                "fg": self.get_color("fg_primary"),
                "borderwidth": 0,
                "cursor": "hand2"
            },
            "info": {
                "bg": self.get_color("accent_info"),
                "fg": "#ffffff",
                "borderwidth": 0,
                "cursor": "hand2"
            }
        }
        return styles.get(style_type, styles["primary"])

# Instance globale du gestionnaire de thème
theme_manager = ThemeManager() 