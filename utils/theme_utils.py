"""
Gestion des thèmes de l'application
"""
import customtkinter as ctk
import darkdetect

def setup_theme():
    """
    Configure le thème de l'application
    
    Returns:
        dict: Dictionnaire contenant les couleurs pour chaque thème
    """
    try:
        # Utiliser le thème système
        system_theme = darkdetect.theme().lower()
        ctk.set_appearance_mode(system_theme)
        
        # Utiliser le thème bleu par défaut
        ctk.set_default_color_theme("blue")
        
        # Définir les couleurs pour chaque thème
        return {
            "light": {
                "bg": "#ffffff",
                "fg": "#000000",
                "entry_bg": "#f0f0f0",
                "frame_bg": "#ffffff",
                "accent": "#2b579a",
                "hover": "#f0f0f0",
                "text": "#000000"
            },
            "dark": {
                "bg": "#1a1a1a",
                "fg": "#ffffff",
                "entry_bg": "#2d2d2d",
                "frame_bg": "#1e1e1e",
                "accent": "#3a7ebf",
                "hover": "#2d2d2d",
                "text": "#ffffff"
            }
        }
        
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
