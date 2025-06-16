import customtkinter as ctk
from typing import Dict
from datetime import datetime
from ui.theme import THEME, FONTS

class DashboardScreen(ctk.CTkFrame):
    """
    Écran du tableau de bord principal avec des indicateurs, graphiques et activités interactives.
    """
    
    def __init__(self, parent, **kwargs):
        """
        Initialise l'écran du tableau de bord.
        
        Args:
            parent: Le widget parent
            **kwargs: Arguments supplémentaires pour le CTkFrame
        """
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.theme_colors = THEME["light"]  # Par défaut, thème clair
        
        # Mettre à jour les couleurs si on est en mode sombre
        if ctk.get_appearance_mode() == "Dark":
            self.theme_colors = THEME["dark"]
            self.configure(fg_color=self.theme_colors["bg"])
            
        print("DEBUG: Initialisation de DashboardScreen")
        
        # Configuration de la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        
        # Créer les sections
        self._create_header()
        self._create_indicators()
        self._create_charts()
        self._create_activities()
    
    def _create_header(self):
        """Crée l'en-tête avec le titre et la date."""
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Tableau de bord",
            font=FONTS["title"],
            text_color=self.theme_colors["text"]
        )
        self.title_label.pack(side="left")
        
        self.date_label = ctk.CTkLabel(
            self.header_frame,
            text=datetime.now().strftime("%A %d %B %Y"),
            font=FONTS["subtitle"],
            text_color=self.theme_colors["subtext"]
        )
        self.date_label.pack(side="right")
    
    def _create_indicators(self):
        """Crée les cartes d'indicateurs statistiques."""
        self.indicators_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.indicators_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        self.indicators_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="cols")
        
        indicators_data = [
            ("📦 Stock total", "1,245 articles", "+12% vs mois dernier", "#4361ee"),
            ("💰 Ventes du mois", "248 ventes", "+8% vs mois dernier", "#4cc9f0"),
            ("⚠️ Alertes", "5 articles en alerte", "Niveau bas", "#f72585")
        ]
        
        self.indicators = {}
        for i, (title, value, subtext, color) in enumerate(indicators_data):
            indicator = self._create_indicator(title, value, subtext, color)
            indicator.grid(row=0, column=i, padx=10, sticky="nsew")
            self.indicators[title.lower().replace(" ", "_")] = indicator
    
    def _create_indicator(self, title: str, value: str, subtext: str, color: str) -> ctk.CTkFrame:
        """
        Crée une carte d'indicateur interactive.
        
        Args:
            title: Titre de l'indicateur
            value: Valeur principale
            subtext: Texte secondaire
            color: Couleur de l'indicateur
            
        Returns:
            Le frame de l'indicateur
        """
        frame = ctk.CTkFrame(
            self.indicators_frame,
            corner_radius=10,
            border_width=1,
            border_color=self.theme_colors["border"]
        )
        
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            inner_frame,
            text=title,
            font=FONTS["subtext"],
            text_color=self.theme_colors["subtext"],
            anchor="w"
        )
        title_label.pack(fill="x")
        
        value_label = ctk.CTkLabel(
            inner_frame,
            text=value,
            font=FONTS["indicator"],
            text_color=self.theme_colors["text"],
            anchor="w"
        )
        value_label.pack(fill="x", pady=(5, 0))
        
        sub_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        sub_frame.pack(fill="x", pady=(5, 0))
        
        color_dot = ctk.CTkLabel(
            sub_frame,
            text="•",
            text_color=color,
            font=("Arial", 20),
            width=10
        )
        color_dot.pack(side="left")
        
        subtext_label = ctk.CTkLabel(
            sub_frame,
            text=subtext,
            font=FONTS["subtext"],
            text_color=self.theme_colors["subtext"],
            anchor="w"
        )
        subtext_label.pack(side="left", fill="x", expand=True)
        
        # Ajouter interactivité
        frame.bind("<Button-1>", lambda e: self._on_indicator_click(title))
        return frame
    
    def _create_charts(self):
        """Crée les graphiques."""
        self.charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        self.charts_frame.grid_columnconfigure(0, weight=2, uniform="chart_cols")
        self.charts_frame.grid_columnconfigure(1, weight=1, uniform="chart_cols")
        
        self.sales_chart = self._create_chart("Ventes des 30 derniers jours", "chart_sales")
        self.sales_chart.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        self.categories_chart = self._create_chart("Répartition par catégorie", "chart_categories")
        self.categories_chart.grid(row=0, column=1, sticky="nsew")
    
    def _create_chart(self, title: str, chart_id: str) -> ctk.CTkFrame:
        """
        Crée un cadre pour un graphique interactif.
        
        Args:
            title: Titre du graphique
            chart_id: Identifiant unique du graphique
            
        Returns:
            Le frame du graphique
        """
        frame = ctk.CTkFrame(
            self.charts_frame,
            corner_radius=10,
            border_width=1,
            border_color=self.theme_colors["border"]
        )
        
        header = ctk.CTkLabel(
            frame,
            text=title,
            font=FONTS["subtitle"],
            text_color=self.theme_colors["text"],
            anchor="w",
            padx=15,
            pady=12
        )
        header.pack(fill="x")
        
        chart = ctk.CTkButton(
            frame,
            text=f"Cliquer pour charger {chart_id}",
            fg_color=self.theme_colors["chart_bg"],
            hover_color=("#e0e0e0", "#333333"),
            font=FONTS["subtext"],
            height=200,
            command=lambda: self._on_chart_click(chart_id)
        )
        chart.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        return frame
    
    def _create_activities(self):
        """Crée la section des dernières activités."""
        self.activities_frame = ctk.CTkFrame(
            self, 
            corner_radius=10,
            fg_color=self.theme_colors["activity_bg"]
        )
        self.activities_frame.grid(row=3, column=0, sticky="nsew")
        self.activities_frame.grid_columnconfigure(0, weight=1)
        
        header = ctk.CTkLabel(
            self.activities_frame,
            text="Dernières activités",
            font=FONTS["subtitle"],
            text_color=self.theme_colors["text"],
            anchor="w",
            padx=20,
            pady=15
        )
        header.pack(fill="x")
        
        self.activities_list = ctk.CTkFrame(
            self.activities_frame, 
            fg_color="transparent"
        )
        self.activities_list.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        activities = [
            ("📦", "Nouvelle entrée", "Ajout de 50 claviers", "Il y a 2 min"),
            ("💰", "Nouvelle vente", "Commande #4587 - 1 250 000 FCFA", "Il y a 15 min"),
            ("⚠️", "Alerte stock", "Souris Logitech - Stock bas", "Il y a 1 h")
        ]
        
        for i, (icon, title, desc, time) in enumerate(activities):
            self._add_activity(icon, title, desc, time, i)
    
    def _add_activity(self, icon: str, title: str, desc: str, time: str, index: int):
        """
        Ajoute une activité interactive à la liste.
        
        Args:
            icon: Icône de l'activité
            title: Titre de l'activité
            desc: Description de l'activité
            time: Temps écoulé
            index: Position dans la liste
        """
        # Utiliser une couleur d'arrière-plan alternée pour les lignes paires
        bg_color = self.theme_colors["activity_bg_alt"] if index % 2 == 0 else "transparent"
        
        activity_frame = ctk.CTkFrame(
            self.activities_list,
            fg_color=bg_color,
            corner_radius=8
        )
        activity_frame.pack(fill="x", pady=2)
        
        container = ctk.CTkFrame(activity_frame, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)
        
        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=("Arial", 16),
            width=30,
            text_color=self.theme_colors["text"]
        )
        icon_label.pack(side="left")
        
        content_frame = ctk.CTkFrame(container, fg_color="transparent")
        content_frame.pack(side="left", fill="x", expand=True)
        
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=FONTS["subtitle"],
            text_color=self.theme_colors["text"],
            anchor="w"
        )
        title_label.pack(fill="x")
        
        desc_label = ctk.CTkLabel(
            content_frame,
            text=desc,
            font=FONTS["subtext"],
            text_color=self.theme_colors["subtext"],
            anchor="w"
        )
        desc_label.pack(fill="x")
        
        time_label = ctk.CTkLabel(
            container,
            text=time,
            font=FONTS["subtext"],
            text_color=self.theme_colors["subtext"],
            anchor="e"
        )
        time_label.pack(side="right")
        
        # Ajouter interactivité
        activity_frame.bind("<Button-1>", lambda e: self._on_activity_click(title, desc))
    
    def _on_indicator_click(self, title: str):
        """Gère le clic sur un indicateur."""
        print(f"DEBUG: Clic sur l'indicateur '{title}'")
        self.title_label.configure(text=f"Tableau de bord - {title}")
    
    def _on_chart_click(self, chart_id: str):
        """Gère le clic sur un graphique."""
        print(f"DEBUG: Clic sur le graphique '{chart_id}'")
        for chart in [self.sales_chart, self.categories_chart]:
            chart.winfo_children()[1].configure(text=f"Graphique {chart_id} chargé")
    
    def _on_activity_click(self, title: str, desc: str):
        """Gère le clic sur une activité."""
        print(f"DEBUG: Clic sur l'activité '{title}': {desc}")
        self.title_label.configure(text=f"Activité: {title}")

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Tableau de bord - UGANC Stock")
    root.geometry("1000x800")
    dashboard = DashboardScreen(root)
    dashboard.pack(fill="both", expand=True, padx=20, pady=20)
    root.mainloop()