import customtkinter as ctk
from tkinter import ttk, messagebox
from typing import Optional, Dict, List, Tuple, Callable

class StockManager(ctk.CTkFrame):
    """
    Interface de gestion du stock avec un design moderne, supportant les modes sombre et clair.
    """
    
    # Constantes de style
    COLORS = {
        "light": {
            "text": "#212529",
            "subtext": "#666666",
            "border": "#e0e0e0",
            "chart_bg": "#f8f9fa",
            "activity_bg": "#f8f9fa",
            "bg": "#f8f9fa",
            "fg": "#ffffff",
            "primary": "#4361ee",
            "primary_hover": "#3a56d4",
            "secondary": "#6c757d",
            "secondary_hover": "#5a6268",
            "success": "#198754",
            "success_bg": "#d1e7dd",
            "warning": "#ffc107",
            "warning_bg": "#fff3cd",
            "danger": "#dc3545",
            "danger_hover": "#bb2d3b",
            "danger_bg": "#f8d7da",
            "table_header": "#f8f9fa",
            "table_selected": "#e9ecef",
            "placeholder_text": "#6c757d"
        },
        "dark": {
            "text": "#f8f9fa",
            "subtext": "#999999",
            "border": "#333333",
            "chart_bg": "#252525",
            "activity_bg": "#252525",
            "bg": "#1a1a1a",
            "fg": "#2d2d2d",
            "primary": "#4cc9f0",
            "primary_hover": "#3ab5d9",
            "secondary": "#6c757d",
            "secondary_hover": "#5a6268",
            "success": "#20c997",
            "success_bg": "#0a3622",
            "warning": "#ffc107",
            "warning_bg": "#664d03",
            "danger": "#f72585",
            "danger_hover": "#d61f74",
            "danger_bg": "#4a0e29",
            "table_header": "#2d2d2d",
            "table_selected": "#3d3d3d",
            "placeholder_text": "#9ca3af"
        }
    }
    FONTS = {
        "title": ("Segoe UI", 24, "bold"),
        "subtitle": ("Segoe UI", 14),
        "subtext": ("Segoe UI", 12),
        "label": ("Segoe UI", 12),
        "label_bold": ("Segoe UI", 12, "bold"),
        "button": ("Segoe UI", 13, "bold"),
        "button_active": ("Segoe UI", 13, "bold"),
        "table": ("Segoe UI", 11),
        "table_header": ("Segoe UI", 11, "bold"),
        "dialog_title": ("Segoe UI", 22, "bold")
    }
    SIZES = {
        "button_width": 120,
        "button_height": 36,
        "filter_button_width": 100,
        "filter_button_height": 32,
        "search_width": 250,
        "dialog_width": 500,
        "dialog_height": 450,
        "table_row_height": 45,
        "padding": 20,
        "small_padding": 10,
        "corner_radius": 10
    }
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_theme = "dark"
        self.configure(fg_color=self.COLORS[self.current_theme]["bg"])
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Données
        self.filter_type = "all"
        self.sort_column = "quantite"
        self.sort_ascending = False
        self.stock_data = []
        
        # Création de l'interface
        print(f"DEBUG: Available COLORS keys: {list(self.COLORS[self.current_theme].keys())}")
        self._create_widgets()
        self._load_sample_data()
        print(f"DEBUG: StockManager initialized in {self.current_theme} mode")
    
    def _create_widgets(self):
        """Crée tous les widgets de l'interface."""
        print("DEBUG: Creating widgets")
        self.header = self._create_header()
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=self.SIZES["padding"], pady=self.SIZES["small_padding"])
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(1, weight=1)
        self._create_toolbar()
        self._create_stock_table()
        self._create_analysis_chart()
    
    def _create_header(self):
        """Crée l'en-tête de la page."""
        print("DEBUG: Creating header")
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=self.SIZES["padding"], pady=(self.SIZES["padding"], self.SIZES["small_padding"]))
        
        title = ctk.CTkLabel(
            header,
            text="📦 Gestion du Stock",
            font=self.FONTS["title"],
            text_color=self.COLORS[self.current_theme]["text"]
        )
        title.pack(side="left")
        
        status_frame = ctk.CTkFrame(header, fg_color="transparent")
        status_frame.pack(side="right")
        
        self.alert_counter = ctk.CTkLabel(
            status_frame,
            text="3 articles en alerte",
            text_color=self.COLORS[self.current_theme]["danger"],
            font=self.FONTS["subtext"]
        )
        self.alert_counter.pack(side="right", padx=self.SIZES["small_padding"])
        
        # Add theme toggle button
        self.theme_btn = ctk.CTkButton(
            status_frame,
            text="☀️ Mode Clair",
            width=self.SIZES["button_width"],
            height=self.SIZES["button_height"],
            fg_color="transparent",
            hover_color=self.COLORS[self.current_theme]["table_selected"],
            text_color=self.COLORS[self.current_theme]["text"],
            border_width=1,
            border_color=self.COLORS[self.current_theme]["border"],
            font=self.FONTS["button"],
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="right", padx=(0, self.SIZES["small_padding"]))
        
        refresh_btn = ctk.CTkButton(
            status_frame,
            text="🔄 Actualiser",
            width=self.SIZES["button_width"],
            height=self.SIZES["button_height"],
            fg_color="transparent",
            hover_color=self.COLORS[self.current_theme]["table_selected"],
            text_color=self.COLORS[self.current_theme]["text"],
            border_width=1,
            border_color=self.COLORS[self.current_theme]["border"],
            font=self.FONTS["button"],
            command=self._refresh_data
        )
        refresh_btn.pack(side="right")
        
        return header
    
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme(new_theme)
        self.theme_btn.configure(text="🌙 Mode Sombre" if new_theme == "light" else "☀️ Mode Clair")
    
    def _create_toolbar(self):
        """Crée la barre d'outils avec les boutons d'action."""
        print("DEBUG: Creating toolbar")
        toolbar = ctk.CTkFrame(self.main_content, fg_color="transparent")
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        filter_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        filter_frame.pack(side="left")
        
        ctk.CTkLabel(
            filter_frame, 
            text="Filtres :",
            font=self.FONTS["label_bold"],
            text_color=self.COLORS[self.current_theme]["text"]
        ).pack(side="left", padx=(0, self.SIZES["small_padding"]))
        
        self.filter_buttons = {}
        filters = [
            ("Tous", "all", self.COLORS[self.current_theme]["secondary"]),
            ("En stock", "in_stock", self.COLORS[self.current_theme]["success"]),
            ("En alerte", "alert", self.COLORS[self.current_theme]["warning"]),
            ("Rupture", "out_of_stock", self.COLORS[self.current_theme]["danger"])
        ]
        
        for text, value, color in filters:
            btn = ctk.CTkButton(
                filter_frame,
                text=text,
                width=self.SIZES["filter_button_width"],
                height=self.SIZES["filter_button_height"],
                fg_color=color,
                hover_color=f"{color[:-2]}CC",
                font=self.FONTS["button"],
                text_color=self.COLORS[self.current_theme]["text"],
                command=lambda v=value: self._apply_filter(v)
            )
            btn.pack(side="left", padx=(0, self.SIZES["small_padding"]))
            self.filter_buttons[value] = btn
        
        action_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        action_frame.pack(side="right")
        
        add_btn = ctk.CTkButton(
            action_frame,
            text="+ Ajouter",
            width=self.SIZES["button_width"],
            height=self.SIZES["button_height"],
            fg_color=self.COLORS[self.current_theme]["primary"],
            hover_color=self.COLORS[self.current_theme]["primary_hover"],
            font=self.FONTS["button"],
            text_color=self.COLORS[self.current_theme]["text"],
            command=self._show_add_dialog
        )
        add_btn.pack(side="left", padx=(0, self.SIZES["small_padding"]))
        
        search_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        search_frame.pack(side="left")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Rechercher un article...",
            width=self.SIZES["search_width"],
            height=self.SIZES["button_height"],
            font=self.FONTS["button"],
            fg_color=self.COLORS[self.current_theme]["fg"],
            text_color=self.COLORS[self.current_theme]["text"],
            placeholder_text_color=self.COLORS[self.current_theme]["placeholder_text"],
            border_width=1,
            border_color=self.COLORS[self.current_theme]["border"]
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", lambda event: self._search_items(event))
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="🔍",
            width=40,
            height=self.SIZES["button_height"],
            fg_color=self.COLORS[self.current_theme]["secondary"],
            hover_color=self.COLORS[self.current_theme]["secondary_hover"],
            font=self.FONTS["button"],
            text_color=self.COLORS[self.current_theme]["text"],
            command=self._search_items
        )
        self.search_btn.pack(side="left")
    
    def _create_stock_table(self):
        """Crée le tableau des stocks."""
        print("DEBUG: Creating stock table")
        table_container = ctk.CTkFrame(self.main_content, fg_color="transparent")
        table_container.grid(row=1, column=0, sticky="nsew")
        table_container.grid_columnconfigure(0, weight=1)
        table_container.grid_rowconfigure(0, weight=1)
        
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure(
            "Custom.Treeview",
            background=self.COLORS[self.current_theme]["activity_bg"],
            foreground=self.COLORS[self.current_theme]["text"],
            rowheight=self.SIZES["table_row_height"],
            fieldbackground=self.COLORS[self.current_theme]["activity_bg"],
            borderwidth=0,
            font=self.FONTS["table"]
        )
        
        style.configure(
            "Custom.Treeview.Heading",
            background=self.COLORS[self.current_theme]["table_header"],
            foreground=self.COLORS[self.current_theme]["text"],
            relief="flat",
            font=self.FONTS["table_header"]
        )
        
        style.map(
            "Custom.Treeview",
            background=[("selected", self.COLORS[self.current_theme]["table_selected"])],
            foreground=[("selected", self.COLORS[self.current_theme]["text"])]
        )
        
        scrollbar = ttk.Scrollbar(table_container)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("reference", "designation", "categorie", "quantite", "seuil", "statut", "actions")
        self.table = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set,
            selectmode="browse",
            style="Custom.Treeview"
        )
        
        self.table.column("reference", width=150, minwidth=120, anchor="w")
        self.table.column("designation", width=250, minwidth=200, anchor="w")
        self.table.column("categorie", width=150, minwidth=120, anchor="w")
        self.table.column("quantite", width=100, minwidth=80, anchor="center")
        self.table.column("seuil", width=80, minwidth=60, anchor="center")
        self.table.column("statut", width=120, minwidth=100, anchor="center")
        self.table.column("actions", width=150, minwidth=120, anchor="center")
        
        self.table.heading("reference", text="Référence", command=lambda: self._sort_table("reference"))
        self.table.heading("designation", text="Désignation", command=lambda: self._sort_table("designation"))
        self.table.heading("categorie", text="Catégorie", command=lambda: self._sort_table("categorie"))
        self.table.heading("quantite", text="Quantité", command=lambda: self._sort_table("quantite"))
        self.table.heading("seuil", text="Seuil", command=lambda: self._sort_table("seuil"))
        self.table.heading("statut", text="Statut", command=lambda: self._sort_table("statut"))
        self.table.heading("actions", text="Actions")
        
        scrollbar.config(command=self.table.yview)
        self.table.pack(fill="both", expand=True)
        
        self.table.tag_configure("in_stock", background=self.COLORS[self.current_theme]["success_bg"])
        self.table.tag_configure("alert", background=self.COLORS[self.current_theme]["warning_bg"])
        self.table.tag_configure("out_of_stock", background=self.COLORS[self.current_theme]["danger_bg"])
        
        self.table.bind("<Double-1>", self._on_item_double_click)
    
    def _create_analysis_chart(self):
        """Crée un graphique d'analyse des stocks."""
        print("DEBUG: Creating analysis chart")
        chart_frame = ctk.CTkFrame(
            self.main_content,
            fg_color=self.COLORS[self.current_theme]["chart_bg"],
            corner_radius=self.SIZES["corner_radius"],
            border_width=1,
            border_color=self.COLORS[self.current_theme]["border"]
        )
        chart_frame.grid(row=2, column=0, sticky="nsew", pady=(15, 0))
        
        ctk.CTkLabel(
            chart_frame,
            text="📊 Aperçu des stocks",
            font=self.FONTS["subtitle"],
            text_color=self.COLORS[self.current_theme]["text"]
        ).pack(pady=self.SIZES["small_padding"], padx=self.SIZES["small_padding"], anchor="w")
        
        # Sample chart data
        in_stock = sum(1 for item in self.stock_data if item["quantite"] > item["seuil"])
        alert = sum(1 for item in self.stock_data if 0 < item["quantite"] <= item["seuil"])
        out_of_stock = sum(1 for item in self.stock_data if item["quantite"] == 0)
        
        # Place your chart widget or visualization code here if needed.
        # The previous chartjs block was not valid Python and has been removed.
    
    def _load_sample_data(self):
        """Charge des données d'exemple pour la démonstration."""
        print("DEBUG: Loading sample data")
        self.stock_data = [
            {"reference": "REF001", "designation": "Ordinateur portable", "categorie": "Informatique", 
             "quantite": 15, "seuil": 5, "statut": "En stock"},
            {"reference": "REF002", "designation": "Souris sans fil", "categorie": "Périphériques", 
             "quantite": 3, "seuil": 5, "statut": "En alerte"},
            {"reference": "REF003", "designation": "Clavier mécanique", "categorie": "Périphériques", 
             "quantite": 0, "seuil": 3, "statut": "Rupture"},
            {"reference": "REF004", "designation": 'Écran 24"', "categorie": "Moniteurs", 
             "quantite": 8, "seuil": 3, "statut": "En stock"},
            {"reference": "REF005", "designation": "Casque audio", "categorie": "Audio", 
             "quantite": 2, "seuil": 4, "statut": "En alerte"},
        ]
        self._update_table()
    
    def _update_table(self):
        """Met à jour le tableau avec les données filtrées et triées."""
        print("DEBUG: Updating table")
        for item in self.table.get_children():
            self.table.delete(item)
        
        filtered_data = self._apply_filters(self.stock_data)
        
        filtered_data.sort(
            key=lambda x: x.get(self.sort_column, ""),
            reverse=not self.sort_ascending
        )
        
        self._update_counters(filtered_data)
        
        for item in filtered_data:
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
        print(f"DEBUG: Applying filter: {filter_type}")
        self.filter_type = filter_type
        self._update_table()
        
        for key, btn in self.filter_buttons.items():
            if key == filter_type:
                btn.configure(
                    fg_color=self.COLORS[self.current_theme]["primary"],
                    hover_color=self.COLORS[self.current_theme]["primary_hover"],
                    font=self.FONTS["button_active"]
                )
            else:
                original_color = self.COLORS[self.current_theme]["secondary"] if key == "all" else \
                                self.COLORS[self.current_theme]["success"] if key == "in_stock" else \
                                self.COLORS[self.current_theme]["warning"] if key == "alert" else \
                                self.COLORS[self.current_theme]["danger"]
                btn.configure(
                    fg_color=original_color,
                    hover_color=f"{original_color[:-2]}CC",
                    font=self.FONTS["button"]
                )
    
    def _sort_table(self, column):
        """Trie le tableau par la colonne sélectionnée."""
        print(f"DEBUG: Sorting table by {column}")
        if self.sort_column == column:
            self.sort_ascending = not self.sort_ascending
        else:
            self.sort_column = column
            self.sort_ascending = True
        self._update_table()
    
    def _search_items(self, event=None):
        """Recherche des articles selon le terme saisi."""
        print("DEBUG: Searching items")
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
        
        self._update_table_with_data(filtered_data)
    
    def _update_table_with_data(self, data):
        """Met à jour le tableau avec les données fournies."""
        print("DEBUG: Updating table with filtered data")
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
        print("DEBUG: Refreshing data")
        self.search_entry.delete(0, "end")
        self.filter_type = "all"
        self._update_table()
        messagebox.showinfo("Actualisation", "Les données ont été actualisées avec succès.")
    
    def _on_item_double_click(self, event):
        """Gère le double-clic sur un article."""
        print("DEBUG: Item double-clicked")
        item = self.table.selection()
        if item:
            values = self.table.item(item, "values")
            if values:
                self._show_edit_dialog(values[0])
    
    def _show_add_dialog(self):
        """Affiche la boîte de dialogue d'ajout d'article."""
        print("DEBUG: Showing add dialog")
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter un article")
        dialog.geometry(f"{self.SIZES['dialog_width']}x{self.SIZES['dialog_height']}")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.COLORS[self.current_theme]["bg"])
        dialog.grab_set()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.SIZES["dialog_width"] // 2)
        y = (screen_height // 2) - (self.SIZES["dialog_height"] // 2)
        dialog.geometry(f"{self.SIZES['dialog_width']}x{self.SIZES['dialog_height']}+{x}+{y}")
        
        ctk.CTkLabel(
            dialog,
            text="Ajouter un nouvel article",
            font=self.FONTS["dialog_title"],
            text_color=self.COLORS[self.current_theme]["text"]
        ).pack(pady=self.SIZES["small_padding"])
        
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=self.SIZES["padding"], pady=self.SIZES["small_padding"], fill="both", expand=True)
        
        fields = [
            ("reference", "Référence", "text"),
            ("designation", "Désignation", "text"),
            ("categorie", "Catégorie", "text"),
            ("quantite", "Quantité", "number"),
            ("seuil", "Seuil d'alerte", "number"),
        ]
        
        entries = {}
        for field, label, ftype in fields:
            ctk.CTkLabel(
                form_frame, 
                text=label + ":",
                font=self.FONTS["label"],
                text_color=self.COLORS[self.current_theme]["text"]
            ).pack(anchor="w", pady=(self.SIZES["small_padding"], 0))
            
            entry = ctk.CTkEntry(
                form_frame,
                placeholder_text=label,
                font=self.FONTS["subtext"],
                fg_color=self.COLORS[self.current_theme]["fg"],
                text_color=self.COLORS[self.current_theme]["text"],
                placeholder_text_color=self.COLORS[self.current_theme]["placeholder_text"],
                border_width=1,
                border_color=self.COLORS[self.current_theme]["border"]
            )
            if ftype == "number":
                entry.configure(validate="key", validatecommand=(dialog.register(self._validate_number), "%P"))
                
            entry.pack(fill="x", pady=(5, 0))
            entries[field] = entry
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=self.SIZES["padding"])
        
        ctk.CTkButton(
            button_frame,
            text="Annuler",
            fg_color=self.COLORS[self.current_theme]["secondary"],
            hover_color=self.COLORS[self.current_theme]["secondary_hover"],
            font=self.FONTS["button"],
            text_color=self.COLORS[self.current_theme]["text"],
            command=dialog.destroy
        ).pack(side="right", padx=self.SIZES["small_padding"])
        
        ctk.CTkButton(
            button_frame,
            text="Enregistrer",
            fg_color=self.COLORS[self.current_theme]["primary"],
            hover_color=self.COLORS[self.current_theme]["primary_hover"],
            font=self.FONTS["button"],
            text_color=self.COLORS[self.current_theme]["text"],
            command=lambda: self._save_new_item(entries, dialog)
        ).pack(side="right")
    
    def _show_edit_dialog(self, reference):
        """Affiche la boîte de dialogue de modification d'article."""
        print(f"DEBUG: Showing edit dialog for {reference}")
        article = next((item for item in self.stock_data if item["reference"] == reference), None)
        if not article:
            messagebox.showerror("Erreur", "Article introuvable.")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Modifier l'article {reference}")
        dialog.geometry(f"{self.SIZES['dialog_width']}x{self.SIZES['dialog_height']}")
        dialog.resizable(False, False)
        dialog.configure(fg_color=self.COLORS[self.current_theme]["bg"])
        dialog.grab_set()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.SIZES["dialog_width"] // 2)
        y = (screen_height // 2) - (self.SIZES["dialog_height"] // 2)
        dialog.geometry(f"{self.SIZES['dialog_width']}x{self.SIZES['dialog_height']}+{x}+{y}")
        
        ctk.CTkLabel(
            dialog,
            text=f"Modifier l'article: {reference}",
            font=self.FONTS["dialog_title"],
            text_color=self.COLORS[self.current_theme]["text"]
        ).pack(pady=self.SIZES["small_padding"])
        
        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=self.SIZES["padding"], pady=self.SIZES["small_padding"], fill="both", expand=True)
        
        fields = [
            ("reference", "Référence", "text", article["reference"]),
            ("designation", "Désignation", "text", article["designation"]),
            ("categorie", "Catégorie", "text", article["categorie"]),
            ("quantite", "Quantité", "number", str(article["quantite"])),
            ("seuil", "Seuil d'alerte", "number", str(article["seuil"])),
        ]
        
        entries = {}
        for field, label, ftype, value in fields:
            ctk.CTkLabel(
                form_frame, 
                text=label + ":",
                font=self.FONTS["label"],
                text_color=self.COLORS[self.current_theme]["text"]
            ).pack(anchor="w", pady=(self.SIZES["small_padding"], 0))
            
            entry = ctk.CTkEntry(
                form_frame,
                placeholder_text=label,
                font=self.FONTS["subtext"],
                fg_color=self.COLORS[self.current_theme]["fg"],
                text_color=self.COLORS[self.current_theme]["text"],
                placeholder_text_color=self.COLORS[self.current_theme]["placeholder_text"],
                border_width=1,
                border_color=self.COLORS[self.current_theme]["border"]
            )
            entry.insert(0, value)
            if ftype == "number":
                entry.configure(validate="key", validatecommand=(dialog.register(self._validate_number), "%P"))
            if field == "reference":
                entry.configure(state="disabled")
                
            entry.pack(fill="x", pady=(5, 0))
            entries[field] = entry
        
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=self.SIZES["padding"])
        
        ctk.CTkButton(
            button_frame,
            text="Supprimer",
            fg_color=self.COLORS[self.current_theme]["danger"],
            hover_color=self.COLORS[self.current_theme]["danger_hover"],
            font=self.FONTS["button"],
            text_color=self.COLORS[self.current_theme]["text"],
            command=lambda: self._confirm_delete(article["reference"], dialog)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Annuler",
            fg_color=self.COLORS[self.current_theme]["secondary"],
            hover_color=self.COLORS[self.current_theme]["secondary_hover"],
            font=self.FONTS["button"],
            text_color=self.COLORS[self.current_theme]["text"],
            command=dialog.destroy
        ).pack(side="right", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Enregistrer",
            fg_color=self.COLORS[self.current_theme]["primary"],
            hover_color=self.COLORS[self.current_theme]["primary_hover"],
            font=self.FONTS["button"],
            text_color=self.COLORS[self.current_theme]["text"],
            command=lambda: self._save_edited_item(article["reference"], entries, dialog)
        ).pack(side="right")
    
    def _save_new_item(self, entries, dialog):
        """Enregistre un nouvel article."""
        print("DEBUG: Saving new item")
        if not all(entry.get().strip() for entry in entries.values()):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        
        new_item = {
            "reference": entries["reference"].get().strip(),
            "designation": entries["designation"].get().strip(),
            "categorie": entries["categorie"].get().strip(),
            "quantite": int(entries["quantite"].get()),
            "seuil": int(entries["seuil"].get()),
            "statut": "En stock"
        }
        
        if any(item["reference"] == new_item["reference"] for item in self.stock_data):
            messagebox.showerror("Erreur", "Une référence d'article identique existe déjà.")
            return
        
        new_item["statut"] = self._calculate_status(new_item)
        self.stock_data.append(new_item)
        self._update_table()
        dialog.destroy()
        messagebox.showinfo("Succès", "L'article a été ajouté avec succès.")
    
    def _save_edited_item(self, old_reference, entries, dialog):
        """Enregistre les modifications d'un article existant."""
        print(f"DEBUG: Saving edited item {old_reference}")
        if not all(entry.get().strip() for field, entry in entries.items() if field != "reference"):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        
        index = next((i for i, item in enumerate(self.stock_data) 
                     if item["reference"] == old_reference), None)
        
        if index is None:
            messagebox.showerror("Erreur", "Article introuvable.")
            return
        
        self.stock_data[index].update({
            "designation": entries["designation"].get().strip(),
            "categorie": entries["categorie"].get().strip(),
            "quantite": int(entries["quantite"].get()),
            "seuil": int(entries["seuil"].get()),
        })
        
        self.stock_data[index]["statut"] = self._calculate_status(self.stock_data[index])
        self._update_table()
        dialog.destroy()
        messagebox.showinfo("Succès", "Les modifications ont été enregistrées avec succès.")
    
    def _confirm_delete(self, reference, dialog):
        """Demande confirmation avant de supprimer un article."""
        print(f"DEBUG: Confirming delete for {reference}")
        if messagebox.askyesno(
            "Confirmer la suppression",
            f"Êtes-vous sûr de vouloir supprimer l'article {reference} ?",
            icon="warning"
        ):
            self._delete_item(reference, dialog)
    
    def _delete_item(self, reference, dialog):
        """Supprime un article de la liste."""
        print(f"DEBUG: Deleting item {reference}")
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
    
    def set_theme(self, theme: str):
        """Change le thème de l'interface."""
        print(f"DEBUG: Changing theme to {theme}")
        self.current_theme = theme.lower() if theme.lower() in ["light", "dark"] else "dark"
        
        # Update main frame
        self.configure(fg_color=self.COLORS[self.current_theme]["bg"])
        self.main_content.configure(fg_color="transparent")
        
        # Update header
        self.header.configure(fg_color="transparent")
        self.header.winfo_children()[0].configure(text_color=self.COLORS[self.current_theme]["text"])  # Title
        self.alert_counter.configure(text_color=self.COLORS[self.current_theme]["danger"])
        self.theme_btn.configure(
            fg_color="transparent",
            hover_color=self.COLORS[self.current_theme]["table_selected"],
            text_color=self.COLORS[self.current_theme]["text"],
            border_color=self.COLORS[self.current_theme]["border"]
        )
        self.header.winfo_children()[1].winfo_children()[1].configure(  # Refresh button
            fg_color="transparent",
            hover_color=self.COLORS[self.current_theme]["table_selected"],
            text_color=self.COLORS[self.current_theme]["text"],
            border_color=self.COLORS[self.current_theme]["border"]
        )
        
        # Update toolbar
        toolbar = self.main_content.winfo_children()[0]
        filter_frame = toolbar.winfo_children()[0]
        filter_frame.winfo_children()[0].configure(text_color=self.COLORS[self.current_theme]["text"])  # Filtres label
        for key, btn in self.filter_buttons.items():
            original_color = self.COLORS[self.current_theme]["secondary"] if key == "all" else \
                            self.COLORS[self.current_theme]["success"] if key == "in_stock" else \
                            self.COLORS[self.current_theme]["warning"] if key == "alert" else \
                            self.COLORS[self.current_theme]["danger"]
            btn.configure(
                fg_color=self.COLORS[self.current_theme]["primary"] if key == self.filter_type else original_color,
                hover_color=f"{original_color[:-2]}CC",
                text_color=self.COLORS[self.current_theme]["text"],
                font=self.FONTS["button_active"] if key == self.filter_type else self.FONTS["button"]
            )
        
        action_frame = toolbar.winfo_children()[1]
        action_frame.winfo_children()[0].configure(  # Add button
            fg_color=self.COLORS[self.current_theme]["primary"],
            hover_color=self.COLORS[self.current_theme]["primary_hover"],
            text_color=self.COLORS[self.current_theme]["text"]
        )
        search_frame = action_frame.winfo_children()[1]
        self.search_entry.configure(
            fg_color=self.COLORS[self.current_theme]["fg"],
            text_color=self.COLORS[self.current_theme]["text"],
            placeholder_text_color=self.COLORS[self.current_theme]["placeholder_text"],
            border_color=self.COLORS[self.current_theme]["border"]
        )
        self.search_btn.configure(
            fg_color=self.COLORS[self.current_theme]["secondary"],
            hover_color=self.COLORS[self.current_theme]["secondary_hover"],
            text_color=self.COLORS[self.current_theme]["text"]
        )
        
        # Update table
        style = ttk.Style()
        style.configure(
            "Custom.Treeview",
            background=self.COLORS[self.current_theme]["activity_bg"],
            foreground=self.COLORS[self.current_theme]["text"],
            fieldbackground=self.COLORS[self.current_theme]["activity_bg"],
            font=self.FONTS["table"]
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=self.COLORS[self.current_theme]["table_header"],
            foreground=self.COLORS[self.current_theme]["text"],
            font=self.FONTS["table_header"]
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", self.COLORS[self.current_theme]["table_selected"])],
            foreground=[("selected", self.COLORS[self.current_theme]["text"])]
        )
        
        self.table.tag_configure("in_stock", background=self.COLORS[self.current_theme]["success_bg"])
        self.table.tag_configure("alert", background=self.COLORS[self.current_theme]["warning_bg"])
        self.table.tag_configure("out_of_stock", background=self.COLORS[self.current_theme]["danger_bg"])
        
        # Recreate chart and update table
        self._create_analysis_chart()
        self._update_table()

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x800")
    stock_manager = StockManager(root)
    stock_manager.pack(fill="both", expand=True)
    root.mainloop()