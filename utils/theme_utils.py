"""
Gestion des thèmes de l'application
"""
import customtkinter as ctk
import darkdetect

def setup_theme():
    """
    Configure le thème de l'application avec une palette moderne
    
    Returns:
        dict: Dictionnaire contenant les couleurs pour chaque thème
    """
    try:
        # Utiliser le thème système
        system_theme = darkdetect.theme().lower()
        ctk.set_appearance_mode(system_theme)
        
        # Palette de couleurs moderne
        COLORS = {
            "light": {
                "primary": "#4361ee",  # Bleu vif
                "secondary": "#3f37c9",  # Bleu foncé
                "success": "#4bb543",    # Vert
                "warning": "#f9c74f",    # Jaune
                "danger": "#ef476f",     # Rouge
                "info": "#4895ef",       # Bleu clair
                "dark": "#212529",        # Noir
                "light": "#f8f9fa",       # Gris très clair
                "bg": "#f8f9fa",
                "card": "#ffffff",
                "text": "#212529",
                "text_secondary": "#6c757d",
                "border": "#dee2e6",
                "hover": "#e9ecef"
            },
            "dark": {
                "primary": "#4361ee",
                "secondary": "#3f37c9",
                "success": "#4bb543",
                "warning": "#f9c74f",
                "danger": "#ef476f",
                "info": "#4895ef",
                "dark": "#212529",
                "light": "#f8f9fa",
                "bg": "#121212",
                "card": "#1e1e1e",
                "text": "#f8f9fa",
                "text_secondary": "#adb5bd",
                "border": "#343a40",
                "hover": "#2d2d2d"
            }
        }
        
        # Configurer CustomTkinter
        ctk.set_default_color_theme("blue")
        
        # Configurer les styles personnalisés
        ctk.set_widget_scaling(1.0)  # Échelle des widgets
        ctk.set_window_scaling(1.0)   # Échelle de la fenêtre
        
        return COLORS
        
        
    except Exception as e:
        print(f"Erreur lors de la configuration du thème: {e}")
        # Valeurs par défaut minimales en cas d'erreur
        return {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "entry_bg": "#f0f0f0",
                "frame_bg": "#ffffff",
                "accent": "#2b579a"
            },
            "dark": {
                "bg": "#1a1a1a",
                "fg": "#ffffff",
                "entry_bg": "#2d2d2d",
                "frame_bg": "#1e1e1e",
                "accent": "#3a7ebf"
            }
        }
