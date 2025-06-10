# ui/main_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
from reporting import report_manager
import sqlite3
from ui.article_form import ArticleManager

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
        if self.current_user["role"].lower() in ["admin", "gestionnaire"]:
            stock_menu.add_command(label="Entrées de stock", command=self.stock_entry)
        stock_menu.add_command(label="Sorties de stock", command=self.stock_exit)
        stock_menu.add_command(label="État du stock", command=self.stock_status)
        menubar.add_cascade(label="Stock", menu=stock_menu)
        
        # Nouveau menu Mouvements (à côté de Stock)
        mouvements_menu = tk.Menu(menubar, tearoff=0)
        mouvements_menu.add_command(label="Historique des entrées", command=self.show_entry_mouvements)
        mouvements_menu.add_command(label="Historique des sorties", command=self.show_exit_mouvements)
        menubar.add_cascade(label="Mouvements", menu=mouvements_menu)
        
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
        ArticleManager(self.root)
    
    def stock_entry(self):
        messagebox.showinfo("Info", "Fonctionnalité d'entrée de stock à implémenter")
    
    def stock_exit(self):
        messagebox.showinfo("Info", "Fonctionnalité de sortie de stock à implémenter")
    
    def stock_status(self):
        # Connexion à la base
        conn = sqlite3.connect("stock_app.db")
        etat = report_manager.get_etat_stocks(conn)
        conn.close()
        # Affichage simple dans une nouvelle fenêtre
        win = tk.Toplevel(self.root)
        win.title("État du stock")
        tree = ttk.Treeview(win, columns=("Code", "Désignation", "Quantité"), show="headings")
        tree.heading("Code", text="Code article")
        tree.heading("Désignation", text="Désignation")
        tree.heading("Quantité", text="Quantité")
        for row in etat:
            tree.insert("", tk.END, values=tuple(row))  # Correction ici
        tree.pack(fill=tk.BOTH, expand=True)
        print("Résultats :", etat)  # ou historique
    
    def system_settings(self):
        messagebox.showinfo("Info", "Fonctionnalité de paramètres système à implémenter")
    
    def view_products(self):
        messagebox.showinfo("Info", "Fonctionnalité de consultation des articles à implémenter")
    
    def show_movement_history(self):
        conn = sqlite3.connect("stock_app.db")
        historique = report_manager.get_historique_mouvements(conn)
        conn.close()
        win = tk.Toplevel(self.root)
        win.title("Historique des mouvements")
        tree = ttk.Treeview(win, columns=("Date", "Code article", "Quantité"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Code article", text="Code article")
        tree.heading("Quantité", text="Quantité")
        for row in historique:
            # row = (date_mvt, type, code_article, quantite)
            tree.insert("", tk.END, values=(row[0], row[2], row[3]))  # On saute row[1] (type)
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_entry_mouvements(self):
        conn = sqlite3.connect("stock_app.db")
        historique = [row for row in report_manager.get_historique_mouvements(conn) if row[1].lower() == "entrée"]
        conn.close()
        win = tk.Toplevel(self.root)
        win.title("Historique des entrées")
        tree = ttk.Treeview(win, columns=("Date", "Code article", "Quantité"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Code article", text="Code article")
        tree.heading("Quantité", text="Quantité")
        for row in historique:
            tree.insert("", tk.END, values=(row[0], row[2], row[3]))  # Correction ici
        tree.pack(fill=tk.BOTH, expand=True)

    def show_exit_mouvements(self):
        conn = sqlite3.connect("stock_app.db")
        historique = [row for row in report_manager.get_historique_mouvements(conn) if row[1].lower() == "sortie"]
        conn.close()
        win = tk.Toplevel(self.root)
        win.title("Historique des sorties")
        tree = ttk.Treeview(win, columns=("Date", "Code article", "Quantité"), show="headings")
        tree.heading("Date", text="Date")
        tree.heading("Code article", text="Code article")
        tree.heading("Quantité", text="Quantité")
        for row in historique:
            tree.insert("", tk.END, values=(row[0], row[2], row[3]))  # On saute row[1] (type)
        tree.pack(fill=tk.BOTH, expand=True)


