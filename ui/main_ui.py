# ui/main_ui.py
import tkinter as tk
from tkinter import ttk, messagebox

class MainUI:
    def __init__(self, root, auth_manager):
        self.root = root
        self.auth_manager = auth_manager
        
        # Récupérer l'utilisateur connecté
        self.current_user = self.auth_manager.get_current_user()
        
        # Configurer la fenêtre principale
        self.root.title(f"Système de Gestion de Stock - {self.current_user['nom_complet']} ({self.current_user['role']})")
        self.root.geometry("800x600")
        
        # Créer les widgets
        self.create_widgets()
        
        # Créer le menu
        self.create_menu()
    
    def create_widgets(self):
        """Crée les widgets de l'interface principale"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Tableau de bord", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Afficher un message de bienvenue
        welcome_label = ttk.Label(main_frame, text=f"Bienvenue, {self.current_user['nom_complet']}!")
        welcome_label.pack(pady=5)
        
        # Créer un notebook pour les différents onglets
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Onglet Tableau de bord
        dashboard_frame = ttk.Frame(notebook, padding="10")
        notebook.add(dashboard_frame, text="Tableau de bord")
        
        # Créer le tableau de bord en fonction du rôle de l'utilisateur
        if self.current_user["role"].lower() == "admin":
            self.create_admin_dashboard(dashboard_frame)
        elif self.current_user["role"].lower() == "gestionnaire":
            self.create_manager_dashboard(dashboard_frame)
        else:
            self.create_seller_dashboard(dashboard_frame)
    
    def create_menu(self):
        """Crée la barre de menu de l'application"""
        menubar = tk.Menu(self.root)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Déconnexion", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.destroy)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        # Menu Gestion (visible pour admin et gestionnaire)
        if self.current_user["role"].lower() in ["admin", "gestionnaire"]:
            management_menu = tk.Menu(menubar, tearoff=0)
            
            # Options pour admin uniquement
            if self.current_user["role"].lower() == "admin":
                management_menu.add_command(label="Gestion des utilisateurs", command=self.manage_users)
                management_menu.add_separator()
            
            management_menu.add_command(label="Gestion des articles", command=self.manage_products)
            menubar.add_cascade(label="Gestion", menu=management_menu)
        
        # Menu Stock
        stock_menu = tk.Menu(menubar, tearoff=0)
        
        # Options pour admin et gestionnaire
        if self.current_user["role"].lower() in ["admin", "gestionnaire"]:
            stock_menu.add_command(label="Entrées de stock", command=self.stock_entry)
        
        # Options pour tous
        stock_menu.add_command(label="Sorties de stock", command=self.stock_exit)
        stock_menu.add_command(label="État du stock", command=self.stock_status)
        menubar.add_cascade(label="Stock", menu=stock_menu)
        
        # Menu Système (admin uniquement)
        if self.current_user["role"].lower() == "admin":
            system_menu = tk.Menu(menubar, tearoff=0)
            system_menu.add_command(label="Paramètres", command=self.system_settings)
            menubar.add_cascade(label="Système", menu=system_menu)
        
        self.root.config(menu=menubar)
    
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
        from ui.user_management import UserManagementUI
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
