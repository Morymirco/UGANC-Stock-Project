# ui/login_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

from auth_manager import AuthManager

class LoginUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Système de Gestion de Stock - Connexion")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
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
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Connexion au Système", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les champs de saisie
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Nom d'utilisateur
        username_label = ttk.Label(input_frame, text="Nom d'utilisateur:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.username_entry = ttk.Entry(input_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5)
        
        # Mot de passe
        password_label = ttk.Label(input_frame, text="Mot de passe:")
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.password_entry = ttk.Entry(input_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        
        # Bouton de connexion
        login_button = ttk.Button(main_frame, text="Se connecter", command=self.login)
        login_button.pack(pady=10)
        
        # Bouton pour créer un nouvel utilisateur (visible uniquement pour les admins)
        self.register_button = ttk.Button(main_frame, text="Créer un utilisateur", command=self.show_register_window)
        self.register_button.pack(pady=5)
        self.register_button.pack_forget()  # Caché par défaut
        
        # Lier la touche Entrée au bouton de connexion
        self.root.bind("<Return>", lambda event: self.login())
    
    def login(self):
        """Gère la tentative de connexion"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        success, message = self.auth_manager.login(username, password)
        if success:
            messagebox.showinfo("Succès", message)
            self.open_main_app()
        else:
            messagebox.showerror("Erreur", message)
    
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
        self.auth_manager.logout()
        self.root.destroy()
    
    def show_register_window(self):
        """Affiche la fenêtre d'enregistrement d'un nouvel utilisateur"""
        register_window = tk.Toplevel(self.root)
        register_window.title("Créer un utilisateur")
        register_window.geometry("400x350")
        register_window.resizable(False, False)
        register_window.transient(self.root)
        register_window.grab_set()
        
        # Centrer la fenêtre
        register_window.update_idletasks()
        width = register_window.winfo_width()
        height = register_window.winfo_height()
        x = (register_window.winfo_screenwidth() // 2) - (width // 2)
        y = (register_window.winfo_screenheight() // 2) - (height // 2)
        register_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(register_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Créer un utilisateur", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les champs de saisie
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Nom d'utilisateur
        username_label = ttk.Label(input_frame, text="Nom d'utilisateur:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        username_entry = ttk.Entry(input_frame, width=30)
        username_entry.grid(row=0, column=1, pady=5)
        
        # Mot de passe
        password_label = ttk.Label(input_frame, text="Mot de passe:")
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        password_entry = ttk.Entry(input_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        # Nom complet
        fullname_label = ttk.Label(input_frame, text="Nom complet:")
        fullname_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        fullname_entry = ttk.Entry(input_frame, width=30)
        fullname_entry.grid(row=2, column=1, pady=5)
        
        # Rôle
        role_label = ttk.Label(input_frame, text="Rôle:")
        role_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        role_combobox = ttk.Combobox(input_frame, width=27, values=["admin", "gestionnaire", "vendeur"])
        role_combobox.grid(row=3, column=1, pady=5)
        role_combobox.current(2)  # Par défaut "vendeur"
        
        # Bouton d'enregistrement
        def register():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            role = role_combobox.get()
            
            if not username or not password or not fullname or not role:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                return
            
            success, message = self.auth_manager.register_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Succès", message)
                register_window.destroy()
            else:
                messagebox.showerror("Erreur", message)
        
        register_button = ttk.Button(main_frame, text="Créer l'utilisateur", command=register)
        register_button.pack(pady=10)


class MainUI:
    def __init__(self, root, auth_manager):
        self.root = root
        self.auth_manager = auth_manager
        
        # Récupérer l'utilisateur connecté
        self.current_user = self.auth_manager.get_current_user()
        
        # Créer les widgets
        self.create_widgets()
    
    def create_widgets(self):
        """Crée les widgets de l'interface principale"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Barre de menu
        self.create_menu()
        
        # Message de bienvenue
        welcome_label = ttk.Label(
            main_frame, 
            text=f"Bienvenue, {self.current_user['nom_complet']} ({self.current_user['role']})",
            font=("Arial", 14)
        )
        welcome_label.pack(pady=10)
        
        # Tableau de bord
        dashboard_frame = ttk.LabelFrame(main_frame, text="Tableau de bord")
        dashboard_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Contenu du tableau de bord en fonction du rôle
        if self.auth_manager.has_permission("admin"):
            self.create_admin_dashboard(dashboard_frame)
        elif self.auth_manager.has_permission("gestionnaire"):
            self.create_manager_dashboard(dashboard_frame)
        else:
            self.create_seller_dashboard(dashboard_frame)
    
    def create_menu(self):
        """Crée la barre de menu de l'application"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Déconnexion", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Menu Articles
        products_menu = tk.Menu(menubar, tearoff=0)
        products_menu.add_command(label="Gérer les articles", command=self.manage_products)
        menubar.add_cascade(label="Articles", menu=products_menu)
        
        # Menu Stock
        stock_menu = tk.Menu(menubar, tearoff=0)
        stock_menu.add_command(label="Entrées de stock", command=self.stock_entry)
        stock_menu.add_command(label="Sorties de stock", command=self.stock_exit)
        stock_menu.add_command(label="État du stock", command=self.stock_status)
        menubar.add_cascade(label="Stock", menu=stock_menu)
        
        # Menu Administration (visible uniquement pour les admins)
        if self.auth_manager.has_permission("admin"):
            admin_menu = tk.Menu(menubar, tearoff=0)
            admin_menu.add_command(label="Gérer les utilisateurs", command=self.manage_users)
            admin_menu.add_command(label="Paramètres système", command=self.system_settings)
            menubar.add_cascade(label="Administration", menu=admin_menu)
    
    def create_admin_dashboard(self, parent):
        """Crée le tableau de bord pour les administrateurs"""
        # Boutons d'accès rapide
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Gérer les utilisateurs", command=self.manage_users).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Gérer les articles", command=self.manage_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="État du stock", command=self.stock_status).pack(side=tk.LEFT, padx=5)
        
        # Statistiques
        stats_frame = ttk.LabelFrame(parent, text="Statistiques")
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(stats_frame, text="Nombre total d'articles: XX").pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text="Valeur totale du stock: XX €").pack(anchor=tk.W, pady=2)
        ttk.Label(stats_frame, text="Nombre d'utilisateurs: XX").pack(anchor=tk.W, pady=2)
    
    def create_manager_dashboard(self, parent):
        """Crée le tableau de bord pour les gestionnaires"""
        # Boutons d'accès rapide
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Gérer les articles", command=self.manage_products).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Entrées de stock", command=self.stock_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="État du stock", command=self.stock_status).pack(side=tk.LEFT, padx=5)
        
        # Alertes de stock
        alerts_frame = ttk.LabelFrame(parent, text="Alertes de stock")
        alerts_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(alerts_frame, text="Articles en rupture de stock: XX").pack(anchor=tk.W, pady=2)
        ttk.Label(alerts_frame, text="Articles sous le seuil d'alerte: XX").pack(anchor=tk.W, pady=2)
    
    def create_seller_dashboard(self, parent):
        """Crée le tableau de bord pour les vendeurs"""
        # Boutons d'accès rapide
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(buttons_frame, text="Sorties de stock", command=self.stock_exit).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Consulter les articles", command=self.view_products).pack(side=tk.LEFT, padx=5)
        
        # Dernières ventes
        sales_frame = ttk.LabelFrame(parent, text="Dernières sorties de stock")
        sales_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Ici, on pourrait afficher un tableau des dernières sorties de stock
        ttk.Label(sales_frame, text="Aucune sortie récente").pack(anchor=tk.CENTER, pady=20)
    
    def logout(self):
        """Déconnecte l'utilisateur et retourne à l'écran de connexion"""
        self.auth_manager.logout()
        self.root.destroy()
        self.root.master.deiconify()  # Afficher à nouveau la fenêtre de connexion
    
    # Méthodes pour les fonctionnalités (à implémenter)
    def manage_users(self):
        # Importer ici pour éviter les importations circulaires
        from user_management import UserManagementUI
        UserManagementUI(self.root, self.auth_manager)
    
    def manage_products(self):
        messagebox.showinfo("Info", "Fonctionnalité de gestion des articles à implémenter")
    
    def stock_entry(self):
        messagebox.showinfo("Info", "Fonctionnalité d'entrée de stock à implémenter")
    
    def stock_exit(self):
        messagebox.showinfo("Info", "Fonctionnalité de sortie de stock à implémenter")
    
    def stock_status(self):
        messagebox.showinfo("Info", "Fonctionnalité d'état du stock à implémenter")
    
    def system_settings(self):
        messagebox.showinfo("Info", "Fonctionnalité de paramètres système à implémenter")
    
    def view_products(self):
        messagebox.showinfo("Info", "Fonctionnalité de consultation des articles à implémenter")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginUI(root)
    root.mainloop()
