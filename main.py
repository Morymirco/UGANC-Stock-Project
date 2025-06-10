#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Point d'entrée principal de l'application de gestion de stock UGANC
"""
import os
import sys
import customtkinter as ctk
from database.db import Database
from ui.login_ui import LoginUI

def main():
    """Fonction principale de l'application"""
    try:
        # Configurer l'apparence de l'application en premier
        ctk.set_appearance_mode("light")  # Forcer le mode clair par défaut
        ctk.set_default_color_theme("blue")  # Thème de couleur par défaut
        
        # Définir les couleurs par défaut pour éviter les erreurs
        ctk.CTkLabel._text_color = "#000000"
        ctk.CTkEntry._fg_color = "#ffffff"
        ctk.CTkButton._fg_color = "#2b579a"
        ctk.CTkButton._hover_color = "#1e3d6d"
        ctk.CTkFrame._fg_color = "#ffffff"
        
        # Initialiser la base de données
        db = Database()
        db.initialize()
        
        # Créer et afficher l'interface de connexion
        # Note: LoginUI crée sa propre fenêtre racine
        LoginUI(None)
        
    except Exception as e:
        print(f"Erreur lors du démarrage de l'application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
