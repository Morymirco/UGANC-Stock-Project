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
        
        # Importer le thème après avoir défini l'apparence
        from ui.theme import THEME, FONTS
        
        # Appliquer les couleurs par défaut du thème
        light_theme = THEME["light"]
        dark_theme = THEME["dark"]
        
        # Configurer les couleurs par défaut de CustomTkinter
        ctk.CTkLabel._text_color = light_theme["text"]
        ctk.CTkLabel._text_color_dark = dark_theme["text"]
        
        ctk.CTkEntry._fg_color = light_theme["entry_bg"]
        ctk.CTkEntry._fg_color_dark = dark_theme["entry_bg"]
        
        ctk.CTkButton._fg_color = light_theme["primary"]
        ctk.CTkButton._fg_color_dark = dark_theme["primary"]
        
        ctk.CTkButton._hover_color = light_theme["primary_hover"]
        ctk.CTkButton._hover_color_dark = dark_theme["primary_hover"]
        
        ctk.CTkFrame._fg_color = light_theme["bg"]
        ctk.CTkFrame._fg_color_dark = dark_theme["bg"]
        
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
