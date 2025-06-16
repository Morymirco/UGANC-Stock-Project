# ui/login_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from core.auth_manager import AuthManager
from ui.main_ui import MainUI
from ui.theme_manager import theme_manager

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion de Stock - Connexion")
        self.root.geometry("450x550")
        self.root.resizable(False, False)
        
        # Configuration des couleurs et du style
        self.setup_styles()
        
        # Configuration de l'arrière-plan
        self.root.configure(bg=theme_manager.get_color("bg_primary"))
        
        # Centrer la fenêtre
        self.center_window()
        
        # Initialiser le gestionnaire d'authentification
        self.auth_manager = AuthManager()
        
        # S'assurer qu'un compte admin existe
        success, message = self.auth_manager.create_admin_if_not_exists()
        if success:
            print(message)
        
        # Créer les widgets
        self.create_widgets()
    
    def setup_styles(self):
        """Configure les styles personnalisés pour l'interface"""
        style = ttk.Style()
        
        # Style pour les boutons principaux
        style.configure('Login.TButton',
                       font=('Arial', 11, 'bold'),
                       background=theme_manager.get_color("accent_success"),
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(10, 8))
        
        style.map('Login.TButton',
                 background=[('active', '#229954'),
                           ('pressed', '#1e8449')])
        
        # Style pour les boutons secondaires
        style.configure('Secondary.TButton',
                       font=('Arial', 10),
                       background=theme_manager.get_color("accent_info"),
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(8, 6))
        
        style.map('Secondary.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#1f618d')])
        
        # Style pour les champs de saisie
        style.configure('Modern.TEntry',
                       font=('Arial', 11),
                       borderwidth=2,
                       relief='solid',
                       fieldbackground=theme_manager.get_color("bg_input"),
                       bordercolor=theme_manager.get_color("border"),
                       focuscolor=theme_manager.get_color("accent_success"),
                       padding=(10, 8))
        
        # Style pour les labels
        style.configure('Title.TLabel',
                       font=('Arial', 20, 'bold'),
                       foreground=theme_manager.get_color("fg_primary"),
                       background=theme_manager.get_color("bg_primary"))
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 12),
                       foreground=theme_manager.get_color("fg_secondary"),
                       background=theme_manager.get_color("bg_primary"))
        
        style.configure('Field.TLabel',
                       font=('Arial', 10, 'bold'),
                       foreground=theme_manager.get_color("fg_primary"),
                       background=theme_manager.get_color("bg_card"))
        
        # Style pour les champs en erreur
        style.configure('Error.TEntry',
                       font=('Arial', 11),
                       borderwidth=2,
                       relief='solid',
                       fieldbackground='#ffebee',
                       bordercolor=theme_manager.get_color("accent_danger"),
                       focuscolor=theme_manager.get_color("accent_danger"),
                       padding=(10, 8))
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Crée les widgets de l'interface de connexion"""
        # Header avec logo
        header_frame = tk.Frame(self.root, bg=theme_manager.get_color("bg_tertiary"), height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Contenu header
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("bg_tertiary"))
        header_content.pack(expand=True)
        
        logo_label = tk.Label(header_content, text="📦", font=('Arial', 32), 
                             bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"))
        logo_label.pack(pady=10)
        
        # Container principal
        main_container = tk.Frame(self.root, bg=theme_manager.get_color("bg_primary"))
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Carte de connexion
        content_frame = tk.Frame(main_container, bg=theme_manager.get_color("bg_card"), relief='solid', bd=1)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Padding intérieur
        inner_frame = tk.Frame(content_frame, bg=theme_manager.get_color("bg_card"))
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Titre
        title_label = tk.Label(inner_frame, text="Connexion", 
                              font=('Arial', 20, 'bold'), bg=theme_manager.get_color("bg_card"), 
                              fg=theme_manager.get_color("fg_primary"))
        title_label.pack(pady=(0, 5))
        
        subtitle_label = tk.Label(inner_frame, text="Accédez à votre espace de gestion", 
                                 font=('Arial', 11), bg=theme_manager.get_color("bg_card"), 
                                 fg=theme_manager.get_color("fg_secondary"))
        subtitle_label.pack(pady=(0, 30))
        
        # Frame pour les champs
        input_frame = tk.Frame(inner_frame, bg=theme_manager.get_color("bg_card"))
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Nom d'utilisateur avec icône
        username_container = tk.Frame(input_frame, bg=theme_manager.get_color("bg_card"))
        username_container.pack(fill=tk.X, pady=(0, 20))
        
        username_label = tk.Label(username_container, text="👤 Nom d'utilisateur", 
                                 font=('Arial', 10, 'bold'), bg=theme_manager.get_color("bg_card"), 
                                 fg=theme_manager.get_color("fg_primary"))
        username_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.username_entry = tk.Entry(username_container, font=('Arial', 11), relief='solid', bd=1,
                                      bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"))
        self.username_entry.pack(fill=tk.X, ipady=8)
        
        # Mot de passe avec icône
        password_container = tk.Frame(input_frame, bg=theme_manager.get_color("bg_card"))
        password_container.pack(fill=tk.X, pady=(0, 25))
        
        password_label = tk.Label(password_container, text="🔒 Mot de passe", 
                                 font=('Arial', 10, 'bold'), bg=theme_manager.get_color("bg_card"), 
                                 fg=theme_manager.get_color("fg_primary"))
        password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = tk.Entry(password_container, show="*", font=('Arial', 11), relief='solid', bd=1,
                                      bg=theme_manager.get_color("bg_input"), fg=theme_manager.get_color("fg_tertiary"))
        self.password_entry.pack(fill=tk.X, ipady=8)
        
        # Boutons
        button_frame = tk.Frame(inner_frame, bg=theme_manager.get_color("bg_card"))
        button_frame.pack(fill=tk.X)
        
        # Bouton de connexion
        login_style = theme_manager.get_button_style("success")
        login_button = tk.Button(button_frame, text="Se connecter", command=self.login, 
                                font=('Arial', 11, 'bold'), **login_style, padx=15, pady=10)
        login_button.pack(fill=tk.X, pady=(10, 15))
        
        # Séparateur
        separator = tk.Frame(button_frame, bg=theme_manager.get_color("separator"), height=1)
        separator.pack(fill=tk.X, pady=15)
        
        # Bouton pour créer un nouvel utilisateur
        secondary_style = theme_manager.get_button_style("info")
        self.register_button = tk.Button(button_frame, text="➕ Créer un utilisateur", 
                                        command=self.show_register_window, 
                                        font=('Arial', 10), **secondary_style, padx=15, pady=8)
        self.register_button.pack(pady=5)
        self.register_button.pack_forget()  # Caché par défaut
        
        # Information en bas
        info_label = tk.Label(inner_frame, 
                             text="Utilisateur par défaut: admin / Mot de passe: admin", 
                             font=('Arial', 10), bg=theme_manager.get_color("bg_card"), 
                             fg=theme_manager.get_color("fg_secondary"))
        info_label.pack(pady=(20, 0))
        
        # Bouton toggle theme
        theme_button = tk.Button(inner_frame, text="🌙 Mode Sombre" if theme_manager.current_theme == "light" else "☀️ Mode Clair",
                                command=self.toggle_theme, font=('Arial', 9),
                                bg=theme_manager.get_color("bg_tertiary"), fg=theme_manager.get_color("fg_primary"),
                                borderwidth=0, cursor='hand2', padx=10, pady=5)
        theme_button.pack(pady=(10, 0))
        
        # Lier la touche Entrée au bouton de connexion
        self.root.bind("<Return>", lambda event: self.login())
        
        # Focus sur le champ username
        self.username_entry.focus()
    
    def toggle_theme(self):
        """Bascule entre les thèmes"""
        theme_manager.toggle_theme()
        # Recréer l'interface avec le nouveau thème
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_styles()
        self.root.configure(bg=theme_manager.get_color("bg_primary"))
        self.create_widgets()
    
    def login(self):
        """Gère la tentative de connexion avec validation visuelle"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Réinitialiser les styles d'erreur
        self.username_entry.configure(bg=theme_manager.get_color("bg_input"), 
                                     fg=theme_manager.get_color("fg_tertiary"))
        self.password_entry.configure(bg=theme_manager.get_color("bg_input"), 
                                     fg=theme_manager.get_color("fg_tertiary"))
        
        if not username or not password:
            if not username:
                self.username_entry.configure(bg='#ffebee', fg='#d32f2f')
            if not password:
                self.password_entry.configure(bg='#ffebee', fg='#d32f2f')
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Trouver le bouton de connexion et changer son texte
        def find_and_update_button(parent, old_text, new_text):
            for widget in parent.winfo_children():
                if isinstance(widget, tk.Button):
                    if old_text in str(widget.cget('text')):
                        widget.configure(text=new_text)
                        return widget
                elif hasattr(widget, 'winfo_children'):
                    result = find_and_update_button(widget, old_text, new_text)
                    if result:
                        return result
            return None
        
        # Afficher un indicateur de chargement
        login_button = find_and_update_button(self.root, "Se connecter", "Connexion en cours...")
        if login_button:
            self.root.update()
        
        success, message = self.auth_manager.login(username, password)
        
        # Restaurer le texte du bouton
        if login_button:
            login_button.configure(text="Se connecter")
        
        if success:
            messagebox.showinfo("Succès", message)
            self.open_main_app()
        else:
            messagebox.showerror("Erreur", message)
            # Effacer le mot de passe en cas d'échec
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def open_main_app(self):
        """Ouvre l'application principale après connexion réussie"""
        self.root.withdraw()  # Cacher la fenêtre de connexion
        
        # Créer une nouvelle fenêtre pour l'application principale
        main_window = tk.Toplevel(self.root)
        main_window.title("Système de Gestion de Stock")
        main_window.geometry("800x600")
        main_window.protocol("WM_DELETE_WINDOW", self.on_main_close)
        
        # Initialiser l'interface principale
        MainUI(main_window, self.auth_manager)
    
    def on_main_close(self):
        """Gère la fermeture de l'application principale"""
        self.root.destroy()  # Fermer complètement l'application
    
    def show_register_window(self):
        """Affiche la fenêtre d'enregistrement d'un nouvel utilisateur"""
        # Créer une nouvelle fenêtre
        register_window = tk.Toplevel(self.root)
        register_window.title("Créer un nouvel utilisateur")
        register_window.geometry("450x450")
        register_window.configure(bg=theme_manager.get_color("bg_primary"))
        register_window.transient(self.root)
        register_window.grab_set()
        
        # Centrer la fenêtre
        register_window.update_idletasks()
        width = register_window.winfo_width()
        height = register_window.winfo_height()
        x = (register_window.winfo_screenwidth() // 2) - (width // 2)
        y = (register_window.winfo_screenheight() // 2) - (height // 2)
        register_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(register_window, bg=theme_manager.get_color("accent_success"), height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg=theme_manager.get_color("accent_success"))
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text="➕ Ajouter un nouvel utilisateur", 
                              font=('Arial', 14, 'bold'), bg=theme_manager.get_color("accent_success"), fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Contenu principal
        main_frame = tk.Frame(register_window, bg=theme_manager.get_color("bg_card"), relief='solid', bd=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content_frame = tk.Frame(main_frame, bg=theme_manager.get_color("bg_card"))
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Frame pour les champs de saisie
        input_frame = tk.Frame(content_frame, bg=theme_manager.get_color("bg_card"))
        input_frame.pack(fill=tk.X, pady=10)
        
        # Champs avec style moderne
        fields = [
            ("👤 Nom d'utilisateur:", 0),
            ("🔒 Mot de passe:", 1),
            ("📝 Nom complet:", 2),
            ("🎭 Rôle:", 3)
        ]
        
        entries = {}
        
        for label_text, row in fields:
            label = tk.Label(input_frame, text=label_text, 
                           font=('Arial', 11, 'bold'), bg=theme_manager.get_color("bg_card"), 
                           fg=theme_manager.get_color("fg_primary"))
            label.grid(row=row, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            if "Rôle" in label_text:
                entry = ttk.Combobox(input_frame, width=25, values=["admin", "gestionnaire", "vendeur"], state="readonly")
                entry.current(2)  # Par défaut "vendeur"
            else:
                entry = tk.Entry(input_frame, font=('Arial', 11), width=28, 
                               relief='solid', bd=1, bg=theme_manager.get_color("bg_input"),
                               fg=theme_manager.get_color("fg_tertiary"))
                if "Mot de passe" in label_text:
                    entry.config(show="*")
            
            entry.grid(row=row, column=1, pady=8)
            entries[row] = entry
        
        # Boutons
        button_frame = tk.Frame(content_frame, bg=theme_manager.get_color("bg_card"))
        button_frame.pack(pady=20)
        
        def register():
            username = entries[0].get().strip()
            password = entries[1].get()
            fullname = entries[2].get().strip()
            role = entries[3].get()
            
            if not username or not password or not fullname or not role:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs", parent=register_window)
                return
            
            success, message = self.auth_manager.register_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Succès", message, parent=register_window)
                register_window.destroy()
            else:
                messagebox.showerror("Erreur", message, parent=register_window)
        
        success_style = theme_manager.get_button_style("success")
        register_button = tk.Button(button_frame, text="✅ Enregistrer", command=register,
                                   font=('Arial', 11, 'bold'), **success_style, padx=20, pady=10)
        register_button.pack(side=tk.LEFT, padx=10)
        
        secondary_style = theme_manager.get_button_style("secondary")
        cancel_button = tk.Button(button_frame, text="❌ Annuler", command=register_window.destroy,
                                 font=('Arial', 11), **secondary_style, padx=20, pady=10)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # Focus sur le premier champ
        entries[0].focus()


