"""
Gestion du stock - Interface moderne avec CustomTkinter
"""
import customtkinter as ctk
from tkinter import ttk, messagebox
from typing import Optional, Dict, List, Tuple, Callable
from utils.theme_utils import get_theme_colors

class StockManager(ctk.CTkFrame):
    """
    Interface de gestion du stock avec un design moderne.
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme_colors = get_theme_colors()
        self.configure(fg_color=self.theme_colors["bg"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Données
        self.filter_type = "all"  # all, low, critical
        self.sort_column = "quantite"
        self.sort_ascending = False
        
        # Création de l'interface
        self._create_widgets()
        self._load_sample_data()
    
    def _create_widgets(self):
        """Crée tous les widgets de l'interface."""
        # En-tête
        self.header = self._create_header()
        
        # Contenu principal
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)
        
        # Barre d'outils
        self._create_toolbar()
        
        # Tableau du stock
        self._create_stock_table()
        
        # Graphique d'analyse (placeholder)
        self._create_analysis_chart()
    
    def _create_header(self):
        """Crée l'en-tête de la page."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Titre
        title = ctk.CTkLabel(
            header,
            text="📦 Gestion du Stock",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(side="left")
        
        # Indicateur de statut
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.pack(side="right")
        
        # Compteur d'articles en alerte
        self.alert_counter = ctk.CTkLabel(
            status_frame,
            text="3 articles en alerte",
            text_color="#ff6b6b",
            font=("Segoe UI", 12)
        )
        self.alert_counter.pack(side="right", padx=10)
        
        # Bouton d'actualisation
        refresh_btn = ctk.CTkButton(
            status_frame,
            text="🔄 Actualiser",
            width=120,
            height=32,
            fg_color="transparent",
            hover_color="#e9ecef",
            text_color=("#2b2b2b", "#f0f0f0"),
            border_width=1,
            border_color=("#dee2e6", "#495057"),
            command=self._refresh_data
        )
        refresh_btn.pack(side="right")
        
        return header
    
    def _create_toolbar(self):
        """Crée la barre d'outils avec les boutons d'action."""
        toolbar = ctk.CTkFrame(self.main_content, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # Groupe de boutons de filtre
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.pack(side="left")
        
        ctk.CTkLabel(
            filter_frame, 
            text="Filtres:",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left", padx=(0, 10))
        
        # Boutons de filtre
        self.filter_buttons = {}
        filters = [
            ("Tous", "all", "#6c757d"),
            ("En stock", "in_stock", "#198754"),
            ("En alerte", "alert", "#fd7e14"),
            ("Rupture", "out_of_stock", "#dc3545")
        ]
        
        for text, value, color in filters:
            btn = ctk.CTkButton(
                filter_frame,
                text=text,
                width=100,
                height=32,
                fg_color=color,
                hover_color=f"{color}CC",
                command=lambda v=value: self._apply_filter(v)
            )
            btn.pack(side="left", padx=(0, 10))
            self.filter_buttons[value] = btn
        
        # Groupe de boutons d'action
        action_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        action_frame.pack(side="right")
        
        # Bouton d'ajout
        add_btn = ctk.CTkButton(
            action_frame,
            text="+ Ajouter",
            width=120,
            height=36,
            fg_color="#0d6efd",
            hover_color="#0b5ed7",
            command=self._show_add_dialog
        )
        add_btn.pack(side="left", padx=(0, 10))
        
        # Champ de recherche
        search_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        search_frame.pack(side="left")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher un article...",
            width=250,
            height=36
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", lambda e: self._search_items())
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=40,
            height=36,
            fg_color="#6c757d",
            hover_color="#5c636a",
            command=self._search_items
        )
        search_btn.pack(side="left")
    
    def _create_stock_table(self):
        """Crée le tableau des stocks."""
        # Conteneur pour le tableau et la barre de défilement
        table_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        table_container.grid(row=1, column=0, sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
        
        # Style pour le tableau
        style = ttk.Style()
        style.theme_use("default")
        
        # Configuration du style de base
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#212529",
            rowheight=45,
            fieldbackground="#ffffff",
            borderwidth=0,
            font=('Segoe UI', 11)
        )
        
        # Style pour les en-têtes
        style.configure(
            "Treeview.Heading",
            background="#f8f9fa",
            foreground="#212529",
            relief="flat",
            font=('Segoe UI', 11, 'bold')
        )
        
        # Style pour les lignes sélectionnées
        style.map(
            'Treeview',
            background=[('selected', '#e9ecef')],
            foreground=[('selected', '#212529')]
        )
        
        # Création de la barre de défilement
        scrollbar = ttk.Scrollbar(table_container)
        scrollbar.pack(side="right", fill="y")
        
        # Création du tableau
        columns = ("reference", "designation", "categorie", "quantite", "seuil", "statut", "actions")
        self.table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse",
            style="Custom.Treeview"
        )
        
        # Configuration des colonnes
        self.table.column("reference", width=150, minwidth=120, anchor="w")
        self.table.column("designation", width=250, minwidth=200, anchor="w")
        self.table.column("categorie", width=150, minwidth=120, anchor="w")
        self.table.column("quantite", width=100, minwidth=80, anchor="center")
        self.table.column("seuil", width=80, minwidth=60, anchor="center")
        self.table.column("statut", width=120, minwidth=100, anchor="center")
        self.table.column("actions", width=150, minwidth=120, anchor="center")
        
        # Configuration des en-têtes
        self.table.heading("reference", text="Référence", command=lambda: self._sort_table("reference"))
        self.table.heading("designation", text="Désignation", command=lambda: self._sort_table("designation"))
        self.table.heading("categorie", text="Catégorie", command=lambda: self._sort_table("categorie"))
        self.table.heading("quantite", text="Quantité", command=lambda: self._sort_table("quantite"))
        self.table.heading("seuil", text="Seuil", command=lambda: self._sort_table("seuil"))
        self.table.heading("statut", text="Statut", command=lambda: self._sort_table("statut"))
        self.table.heading("actions", text="Actions")
        
        # Configuration de la barre de défilement
        scrollbar.config(command=self.table.yview)
        
        # Ajout du tableau au conteneur
        self.table.pack(fill="both", expand=True)
        
        # Configuration des tags pour les statuts
        self.table.tag_configure('in_stock', background='#d1e7dd')
        self.table.tag_configure('alert', background='#fff3cd')
        self.table.tag_configure('out_of_stock', background='#f8d7da')
        
        # Événements
        self.table.bind("<Double-1>", self._on_item_double_click)
    
    def _create_analysis_chart(self):
        """Crée un graphique d'analyse (placeholder)."""
        chart_frame = ctk.CTkFrame(
            self.main_content,
            fg_color="#f8f9fa",
            corner_radius=10,
            border_width=1,
            border_color="#dee2e6"
        )
        chart_frame.grid(row=2, column=0, sticky="nsew", pady=(15, 0))
        
        # Titre du graphique
        ctk.CTkLabel(
            chart_frame,
            text="📊 Aperçu des stocks",
            font=("Segoe UI", 14, "bold"),
            text_color=("#2b2b2b", "#f0f0f0")
        ).pack(pady=15, padx=15, anchor="w")
        
        # Zone du graphique (placeholder)
        chart_placeholder = ctk.CTkLabel(
            chart_frame,
            text="Graphique d'analyse des stocks\n(À implémenter avec Matplotlib/Plotly)",
            text_color=("#6c757d", "#adb5bd"),
            font=("Segoe UI", 12),
            justify="center"
        )
        chart_placeholder.pack(expand=True, fill="both", pady=30)
        
        # Légende
        legend_frame = ctk.CTkFrame(chart_frame, fg_color="transparent")
        legend_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Données d'exemple pour la démonstration
        self.stock_data = []
        self._load_sample_data()
        
    def _load_sample_data(self):
        """Charge des données d'exemple pour la démonstration."""
        self.stock_data = [
            {"reference": "REF001", "designation": "Ordinateur portable", "categorie": "Informatique", 
             "quantite": 15, "seuil": 5, "statut": "En stock"},
            {"reference": "REF002", "designation": "Souris sans fil", "categorie": "Périphériques", 
             "quantite": 3, "seuil": 5, "statut": "En alerte"},
            {"reference": "REF003", "designation": "Clavier mécanique", "categorie": "Périphériques", 
             "quantite": 0, "seuil": 3, "statut": "Rupture"},
            {"reference": "REF004", "designation": "Écran 24\"", "categorie": "Moniteurs", 
             "quantite": 8, "seuil": 3, "statut": "En stock"},
            {"reference": "REF005", "designation": "Casque audio", "categorie": "Audio", 
             "quantite": 2, "seuil": 4, "statut": "En alerte"},
        ]
        self._update_table()
    
    def _update_table(self):
        """Met à jour le tableau avec les données filtrées et triées."""
        # Effacer les données actuelles
        for item in self.table.get_children():
            self.table.delete(item)
        
        # Appliquer le filtre
        filtered_data = self._apply_filters(self.stock_data)
        
        # Appliquer le tri
        filtered_data.sort(
            key=lambda x: x.get(self.sort_column, ""),
            reverse=not self.sort_ascending
        )
        
        # Mettre à jour les compteurs
        self._update_counters(filtered_data)
        
        # Ajouter les données au tableau
        for item in filtered_data:
            tag = self._get_status_tag(item)
            values = (
                item["reference"],
                item["designation"],
                item["categorie"],
                item["quantite"],
                item["seuil"],
                item["statut"],
                "✏️ | 🗑️"  # Actions: Éditer | Supprimer
            )
            self.table.insert("", "end", values=values, tags=(tag,))
    
    def _apply_filters(self, data):
        """Applique les filtres actuels aux données."""
        if self.filter_type == "all":
            return data
        elif self.filter_type == "in_stock":
            return [item for item in data if item["quantite"] > item["seuil"]]
        elif self.filter_type == "alert":
            return [item for item in data if 0 < item["quantite"] <= item["seuil"]]
        elif self.filter_type == "out_of_stock":
            return [item for item in data if item["quantite"] == 0]
        return data
    
    def _update_counters(self, data):
        """Met à jour les compteurs d'alertes."""
        alert_count = sum(1 for item in data if 0 < item["quantite"] <= item["seuil"])
        out_of_stock_count = sum(1 for item in data if item["quantite"] == 0)
        self.alert_counter.configure(text=f"{alert_count} articles en alerte • {out_of_stock_count} en rupture")
    
    def _get_status_tag(self, item):
        """Retourne le tag de statut pour un article."""
        if item["quantite"] == 0:
            return "out_of_stock"
        elif item["quantite"] <= item["seuil"]:
            return "alert"
        return "in_stock"
    
    def _apply_filter(self, filter_type):
        """Applique le filtre sélectionné."""
        self.filter_type = filter_type
        self._update_table()
        
        # Mettre à jour l'apparence des boutons de filtre
        for key, btn in self.filter_buttons.items():
            if key == filter_type:
                btn.configure(fg_color="#0d6efd")
            else:
                btn.configure(fg_color=btn.cget("hover_color").replace("CC", ""))
    
    def _sort_table(self, column):
        """Trie le tableau par la colonne sélectionnée."""
        if self.sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column
            self.sort_ascending = True
        self._update_table()
    
    def _search_items(self):
        """Recherche des articles selon le terme saisi."""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self._update_table()
            return
        
        filtered_data = [
            item for item in self.stock_data
            if (search_term in item["reference"].lower() or 
                 search_term in item["designation"].lower() or
                 search_term in item["categorie"].lower())
        ]
        
        # Mettre à jour le tableau avec les résultats de la recherche
        self._update_table_with_data(filtered_data)
    
    def _update_table_with_data(self, data):
        """Met à jour le tableau avec les données fournies."""
        for item in self.table.get_children():
            self.table.delete(item)
            
        for item in data:
            tag = self._get_status_tag(item)
            values = (
                item["reference"],
                item["designation"],
                item["categorie"],
                item["quantite"],
                item["seuil"],
                item["statut"],
                "✏️ | 🗑️"
            )
            self.table.insert("", "end", values=values, tags=(tag,))
    
    def _refresh_data(self):
        """Rafraîchit les données du tableau."""
        self.search_entry.delete(0, "end")
        self.filter_type = "all"
        self._update_table()
        messagebox.showinfo("Actualisation", "Les données ont été actualisées avec succès.")
    
    def _on_item_double_click(self, event):
        """Gère le double-clic sur un article."""
        item = self.table.selection()
        if item:
            values = self.table.item(item, "values")
            if values:
                self._show_edit_dialog(values[0])  # Passer la référence de l'article
    
    def _show_add_dialog(self):
        """Affiche la boîte de dialogue d'ajout d'article."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter un article")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.grab_set()  # Rend la fenêtre modale
        
        # Centrer la fenêtre
        window_width = 500
        window_height = 450
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Contenu de la boîte de dialogue
        ctk.CTkLabel(
            dialog,
            text="Ajouter un nouvel article",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)
        
        # Formulaire
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Champs du formulaire
        fields = [
            ("reference", "Référence", "text"),
            ("designation", "Désignation", "text"),
            ("categorie", "Catégorie", "text"),
            ("quantite", "Quantité", "number"),
            ("seuil", "Seuil d'alerte", "number"),
        ]
        
        entries = {}
        for field, label, ftype in fields:
            ctk.CTkLabel(form_frame, text=label + ":").pack(anchor="w", pady=(10, 0))
            
            if ftype == "number":
                entry = ctk.CTkEntry(form_frame, placeholder_text=label)
                entry.configure(validate="key", validatecommand=(dialog.register(self._validate_number), "%P"))
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text=label)
                
            entry.pack(fill="x", pady=(5, 0))
            entries[field] = entry
        
        # Boutons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(
            button_frame,
            text="Annuler",
            fg_color="#6c757d",
            hover_color="#5c636a",
            command=dialog.destroy
        ).pack(side="right", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Enregistrer",
            fg_color="#0d6efd",
            hover_color="#0b5ed7",
            command=lambda: self._save_new_item(entries, dialog)
        ).pack(side="right")
    
    def _show_edit_dialog(self, reference):
        """Affiche la boîte de dialogue de modification d'article."""
        # Trouver l'article à modifier
        article = next((item for item in self.stock_data if item["reference"] == reference), None)
        if not article:
            messagebox.showerror("Erreur", "Article introuvable.")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Modifier l'article {reference}")
        dialog.geometry("500x450")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # Centrer la fenêtre
        window_width = 500
        window_height = 450
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Contenu de la boîte de dialogue
        ctk.CTkLabel(
            dialog,
            text=f"Modifier l'article: {reference}",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=15)
        
        # Formulaire
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Champs du formulaire
        fields = [
            ("reference", "Référence", "text", article["reference"]),
            ("designation", "Désignation", "text", article["designation"]),
            ("categorie", "Catégorie", "text", article["categorie"]),
            ("quantite", "Quantité", "number", str(article["quantite"])),
            ("seuil", "Seuil d'alerte", "number", str(article["seuil"])),
        ]
        
        entries = {}
        for field, label, ftype, value in fields:
            ctk.CTkLabel(form_frame, text=label + ":").pack(anchor="w", pady=(10, 0))
            
            if ftype == "number":
                entry = ctk.CTkEntry(form_frame, placeholder_text=label)
                entry.insert(0, value)
                entry.configure(validate="key", validatecommand=(dialog.register(self._validate_number), "%P"))
            else:
                entry = ctk.CTkEntry(form_frame, placeholder_text=label)
                entry.insert(0, value)
                if field == "reference":  # La référence ne peut pas être modifiée
                    entry.configure(state="disabled")
                
            entry.pack(fill="x", pady=(5, 0))
            entries[field] = entry
        
        # Boutons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Bouton Supprimer
        ctk.CTkButton(
            button_frame,
            text="Supprimer",
            fg_color="#dc3545",
            hover_color="#bb2d3b",
            command=lambda: self._confirm_delete(article["reference"], dialog)
        ).pack(side="left", padx=5)
        
        # Bouton Annuler
        ctk.CTkButton(
            button_frame,
            text="Annuler",
            fg_color="#6c757d",
            hover_color="#5c636a",
            command=dialog.destroy
        ).pack(side="right", padx=5)
        
        # Bouton Enregistrer
        ctk.CTkButton(
            button_frame,
            text="Enregistrer",
            fg_color="#0d6efd",
            hover_color="#0b5ed7",
            command=lambda: self._save_edited_item(article["reference"], entries, dialog)
        ).pack(side="right", padx=5)
    
    def _save_new_item(self, entries, dialog):
        """Enregistre un nouvel article."""
        # Validation des champs
        if not all(entry.get().strip() for entry in entries.values()):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        
        # Création du nouvel article
        new_item = {
            "reference": entries["reference"].get().strip(),
            "designation": entries["designation"].get().strip(),
            "categorie": entries["categorie"].get().strip(),
            "quantite": int(entries["quantite"].get()),
            "seuil": int(entries["seuil"].get()),
            "statut": "En stock"  # Mis à jour plus tard
        }
        
        # Vérifier si la référence existe déjà
        if any(item["reference"] == new_item["reference"] for item in self.stock_data):
            messagebox.showerror("Erreur", "Une référence d'article identique existe déjà.")
            return
        
        # Mettre à jour le statut
        new_item["statut"] = self._calculate_status(new_item)
        
        # Ajouter à la liste des données
        self.stock_data.append(new_item)
        
        # Mettre à jour l'interface
        self._update_table()
        dialog.destroy()
        messagebox.showinfo("Succès", "L'article a été ajouté avec succès.")
    
    def _save_edited_item(self, old_reference, entries, dialog):
        """Enregistre les modifications d'un article existant."""
        # Validation des champs
        if not all(entry.get().strip() for field, entry in entries.items() if field != "reference"):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        
        # Trouver l'index de l'article à modifier
        index = next((i for i, item in enumerate(self.stock_data) 
                     if item["reference"] == old_reference), None)
        
        if index is None:
            messagebox.showerror("Erreur", "Article introuvable.")
            return
        
        # Mettre à jour l'article
        self.stock_data[index].update({
            "designation": entries["designation"].get().strip(),
            "categorie": entries["categorie"].get().strip(),
            "quantite": int(entries["quantite"].get()),
            "seuil": int(entries["seuil"].get()),
        })
        
        # Mettre à jour le statut
        self.stock_data[index]["statut"] = self._calculate_status(self.stock_data[index])
        
        # Mettre à jour l'interface
        self._update_table()
        dialog.destroy()
        messagebox.showinfo("Succès", "Les modifications ont été enregistrées avec succès.")
    
    def _confirm_delete(self, reference, dialog):
        """Demande confirmation avant de supprimer un article."""
        if messagebox.askyesno(
            "Confirmer la suppression",
            f"Êtes-vous sûr de vouloir supprimer l'article {reference} ?",
            icon="warning"
        ):
            self._delete_item(reference, dialog)
    
    def _delete_item(self, reference, dialog):
        """Supprime un article de la liste."""
        self.stock_data = [item for item in self.stock_data if item["reference"] != reference]
        self._update_table()
        dialog.destroy()
        messagebox.showinfo("Succès", "L'article a été supprimé avec succès.")
    
    def _calculate_status(self, item):
        """Calcule le statut d'un article en fonction de sa quantité et de son seuil."""
        if item["quantite"] == 0:
            return "Rupture"
        elif item["quantite"] <= item["seuil"]:
            return "En alerte"
        return "En stock"
    
    @staticmethod
    def _validate_number(value):
        """Valide que la valeur est un nombre positif ou vide."""
        if value == "":
            return True
        try:
            return int(value) >= 0
        except ValueError:
            return False