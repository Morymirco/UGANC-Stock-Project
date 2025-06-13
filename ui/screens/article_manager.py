"""
Gestion des articles - Interface moderne avec CustomTkinter
"""
import customtkinter as ctk
from tkinter import ttk
from typing import Optional, Dict, List, Tuple, Callable
from utils.theme_utils import setup_theme

class ArticleManager(ctk.CTkFrame):
    """
    Interface de gestion des articles avec un design moderne.
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme_colors = setup_theme()
        self.configure(fg_color=self.theme_colors["bg"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # En-tête
        self.header = self._create_header()
        
        # Contenu principal
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)
        
        # Barre d'outils
        self.toolbar = self._create_toolbar()
        
        # Tableau des articles
        self.article_table = self._create_article_table()
        
        # Formulaire d'ajout/modification
        self.form_frame = None
    
    def _create_header(self) -> ctk.CTkFrame:
        """Crée l'en-tête de la page."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header,
            text="Gestion des Articles",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(side="left")
        
        return header
    
    def _create_toolbar(self) -> ctk.CTkFrame:
        """Crée la barre d'outils avec les boutons d'action."""
        toolbar = ctk.CTkFrame(self.main_content, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # Bouton Nouvel Article
        add_btn = ctk.CTkButton(
            toolbar,
            text="+ Nouvel Article",
            command=self._show_add_article_form,
            fg_color=self.theme_colors["primary"],
            hover_color=self.theme_colors["primary_dark"],
            height=36
        )
        add_btn.pack(side="left", padx=(0, 10))
        
        # Champ de recherche
        search_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        search_frame.pack(side="right", fill="x", expand=True)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher un article...",
            width=300,
            height=36
        )
        search_entry.pack(side="right")
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=40,
            height=36,
            fg_color=self.theme_colors["secondary"],
            hover_color=self.theme_colors["secondary_dark"]
        )
        search_btn.pack(side="right", padx=(0, 5))
        
        return toolbar
    
    def _create_article_table(self) -> ttk.Treeview:
        """Crée le tableau des articles."""
        container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        
        # Style pour le tableau
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#FFFFFF",
            foreground="black",
            rowheight=40,
            fieldbackground="#FFFFFF",
            borderwidth=0
        )
        style.map(
            'Treeview',
            background=[('selected', self.theme_colors["primary_light"])],
            foreground=[('selected', 'black')]
        )
        
        # Création du Treeview avec une barre de défilement
        tree_scroll = ctk.CTkScrollbar(container)
        tree_scroll.pack(side="right", fill="y")
        
        columns = ("code", "designation", "categorie", "prix_achat", "prix_vente", "stock")
        tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings",
            yscrollcommand=tree_scroll.set,
            selectmode="browse"
        )
        
        # Configuration des colonnes
        tree.column("code", width=120, minwidth=100)
        tree.column("designation", width=250, minwidth=200)
        tree.column("categorie", width=150, minwidth=120)
        tree.column("prix_achat", width=120, minwidth=100, anchor="e")
        tree.column("prix_vente", width=120, minwidth=100, anchor="e")
        tree.column("stock", width=100, minwidth=80, anchor="center")
        
        # En-têtes des colonnes
        tree.heading("code", text="Code Article")
        tree.heading("designation", text="Désignation")
        tree.heading("categorie", text="Catégorie")
        tree.heading("prix_achat", text="Prix d'achat")
        tree.heading("prix_vente", text="Prix de vente")
        tree.heading("stock", text="Stock")
        
        # Ajout de données de test (à remplacer par les vraies données)
        self._add_sample_data(tree)
        
        tree.pack(fill="both", expand=True)
        tree_scroll.configure(command=tree.yview)
        
        # Ajout d'un événement de clic
        tree.bind("<Double-1>", self._on_item_double_click)
        
        return tree
    
    def _add_sample_data(self, tree: ttk.Treeview):
        """Ajoute des données de test au tableau."""
        sample_data = [
            ("ART001", "Ordinateur portable", "Informatique", 800.0, 1200.0, 15),
            ("ART002", "Souris sans fil", "Périphériques", 25.0, 45.0, 42),
            ("ART003", "Clavier mécanique", "Périphériques", 50.0, 89.99, 23),
            ("ART004", "Écran 24\"", "Moniteurs", 150.0, 249.99, 8),
            ("ART005", "Casque audio", "Audio", 75.0, 129.99, 17),
        ]
        
        for item in sample_data:
            tree.insert("", "end", values=item)
    
    def _show_add_article_form(self):
        """Affiche le formulaire d'ajout d'article."""
        if self.form_frame:
            self.form_frame.destroy()
        
        self.form_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="#FFFFFF",
            corner_radius=10,
            border_width=1,
            border_color=self.theme_colors["border"]
        )
        self.form_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        # Titre du formulaire
        title = ctk.CTkLabel(
            self.form_frame,
            text="Nouvel Article",
            font=("Segoe UI", 16, "bold"),
            text_color=self.theme_colors["text"]
        )
        title.pack(pady=(20, 15), padx=20, anchor="w")
        
        # Formulaire
        form_fields = [
            ("Code Article", "entry"),
            ("Désignation", "entry"),
            ("Catégorie", "combobox"),
            ("Prix d'achat (€)", "entry"),
            ("Prix de vente (€)", "entry"),
            ("Seuil d'alerte", "entry"),
            ("Description", "text")
        ]
        
        for i, (label, field_type) in enumerate(form_fields):
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=5)
            
            lbl = ctk.CTkLabel(
                frame,
                text=label,
                width=120,
                anchor="w"
            )
            lbl.pack(side="left", padx=(0, 10))
            
            if field_type == "entry":
                entry = ctk.CTkEntry(
                    frame,
                    height=36,
                    fg_color="#FFFFFF",
                    text_color="#000000",
                    border_width=1,
                    corner_radius=4
                )
                entry.pack(side="right", fill="x", expand=True)
            
            elif field_type == "combobox":
                combobox = ctk.CTkComboBox(
                    frame,
                    values=["Informatique", "Périphériques", "Réseau", "Bureautique"],
                    height=36,
                    fg_color="#FFFFFF",
                    text_color="#000000",
                    button_color=self.theme_colors["primary"],
                    button_hover_color=self.theme_colors["primary_dark"]
                )
                combobox.pack(side="right", fill="x", expand=True)
            
            elif field_type == "text":
                text = ctk.CTkTextbox(
                    frame,
                    height=80,
                    fg_color="#FFFFFF",
                    text_color="#000000",
                    border_width=1,
                    corner_radius=4
                )
                text.pack(side="right", fill="x", expand=True)
        
        # Boutons d'action
        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Annuler",
            fg_color="#6c757d",
            hover_color="#5a6268",
            command=lambda: self.form_frame.destroy()
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        save_btn = ctk.CTkButton(
            btn_frame,
            text="Enregistrer",
            fg_color=self.theme_colors["primary"],
            hover_color=self.theme_colors["primary_dark"]
        )
        save_btn.pack(side="right")
    
    def _on_item_double_click(self, event):
        """Gère le double-clic sur un article."""
        item = self.article_table.selection()[0]
        values = self.article_table.item(item, "values")
        self._show_edit_article_form(values)
    
    def _show_edit_article_form(self, article_data):
        """Affiche le formulaire de modification d'article."""
        self._show_add_article_form()  # Même formulaire que pour l'ajout
        
        # Mettre à jour le titre
        for widget in self.form_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "Nouvel Article":
                widget.configure(text="Modifier l'article")
                break
        
        # Remplir les champs avec les données existantes
        # (à implémenter avec les vraies données)

    def refresh_data(self):
        """Rafraîchit les données du tableau."""
        # À implémenter: charger les données depuis la base de données
        pass

if __name__ == "__main__":
    # Exemple d'utilisation
    root = ctk.CTk()
    root.title("Tableau de bord - UGANC Stock")
    root.geometry("1000x800")
    
    # Créer l'écran du tableau de bord
    dashboard = ArticleManager(root)
    dashboard.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Démarrer la boucle principale
    root.mainloop()