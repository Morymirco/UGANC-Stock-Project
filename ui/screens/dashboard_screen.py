"""
Écran du tableau de bord principal de l'application.
"""
import customtkinter as ctk
from typing import Dict, Any
from datetime import datetime

class DashboardScreen(ctk.CTkFrame):
    """
    Écran du tableau de bord principal avec des indicateurs et des graphiques.
    """
    
    def __init__(self, parent, **kwargs):
        """
        Initialise l'écran du tableau de bord.
        
        Args:
            parent: Le widget parent
            **kwargs: Arguments supplémentaires pour le CTkFrame
        """
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # En-tête
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        
        # Titre et date
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Tableau de bord",
            font=("Segoe UI", 24, "bold")
        )
        self.title_label.pack(side="left")
        
        self.date_label = ctk.CTkLabel(
            self.header_frame,
            text=datetime.now().strftime("%A %d %B %Y"),
            font=("Segoe UI", 14),
            text_color=("#666666", "#999999")
        )
        self.date_label.pack(side="right")
        
        # Grille pour les indicateurs
        self.indicators_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.indicators_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        # Configuration de la grille des indicateurs
        for i in range(3):
            self.indicators_frame.grid_columnconfigure(i, weight=1, uniform="cols")
        
        # Indicateurs (cartes statistiques)
        self.indicators = {
            "total_stock": self._create_indicator(
                "📦 Stock total", "1,245 articles", "+12% vs mois dernier", "#4361ee"
            ),
            "ventes_mois": self._create_indicator(
                "💰 Ventes du mois", "248 ventes", "+8% vs mois dernier", "#4cc9f0"
            ),
            "alertes": self._create_indicator(
                "⚠️ Alertes", "5 articles en alerte", "Niveau bas", "#f72585"
            )
        }
        
        # Positionner les indicateurs
        for i, (_, indicator) in enumerate(self.indicators.items()):
            indicator.grid(row=0, column=i, padx=10, sticky="nsew")
        
        # Graphiques
        self.charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.charts_frame.grid(row=2, column=0, sticky="nsew")
        self.charts_frame.grid_columnconfigure(0, weight=2, uniform="chart_cols")
        self.charts_frame.grid_columnconfigure(1, weight=1, uniform="chart_cols")
        
        # Graphique des ventes
        self.sales_chart = self._create_chart(
            self.charts_frame, "Ventes des 30 derniers jours", "chart_sales"
        )
        self.sales_chart.grid(row=0, column=0, padx=(0, 10), pady=(0, 20), sticky="nsew")
        
        # Graphique des catégories
        self.categories_chart = self._create_chart(
            self.charts_frame, "Répartition par catégorie", "chart_categories"
        )
        self.categories_chart.grid(row=0, column=1, pady=(0, 20), sticky="nsew")
        
        # Dernières activités
        self.activities_frame = ctk.CTkFrame(self, corner_radius=10)
        self.activities_frame.grid(row=3, column=0, sticky="nsew")
        self.activities_frame.grid_columnconfigure(0, weight=1)
        
        # En-tête des activités
        activities_header = ctk.CTkLabel(
            self.activities_frame,
            text="Dernières activités",
            font=("Segoe UI", 16, "bold"),
            anchor="w",
            padx=20,
            pady=15
        )
        activities_header.grid(row=0, column=0, sticky="ew")
        
        # Liste des activités
        self.activities_list = ctk.CTkFrame(
            self.activities_frame, 
            fg_color="transparent"
        )
        self.activities_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Exemples d'activités
        activities = [
            ("📦", "Nouvelle entrée en stock", "Ajout de 50 unités de Clavier mécanique", "Il y a 2 minutes"),
            ("💰", "Nouvelle vente", "Commande #4587 - 1 250 000 FCFA", "Il y a 15 minutes"),
            ("⚠️", "Alerte stock bas", "Souris Logitech - Seuil minimum atteint", "Il y a 1 heure")
        ]
        
        for i, (icon, title, desc, time) in enumerate(activities):
            self._add_activity(icon, title, desc, time, i)
    
    def _create_indicator(self, title: str, value: str, subtext: str, color: str) -> ctk.CTkFrame:
        """
        Crée une carte d'indicateur.
        
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
            border_color=("#e0e0e0", "#333333")
        )
        
        # Conteneur interne
        inner_frame = ctk.CTkFrame(frame, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            inner_frame,
            text=title,
            font=("Segoe UI", 12),
            text_color=("#666666", "#999999"),
            anchor="w"
        )
        title_label.pack(fill="x")
        
        # Valeur
        value_label = ctk.CTkLabel(
            inner_frame,
            text=value,
            font=("Segoe UI", 22, "bold"),
            anchor="w"
        )
        value_label.pack(fill="x", pady=(5, 0))
        
        # Texte secondaire avec indicateur de couleur
        sub_frame = ctk.CTkFrame(inner_frame, fg_color="transparent")
        sub_frame.pack(fill="x", pady=(5, 0))
        
        # Point de couleur
        color_dot = ctk.CTkLabel(
            sub_frame,
            text="•",
            text_color=color,
            font=("Arial", 20),
            width=10
        )
        color_dot.pack(side="left")
        
        # Texte
        subtext_label = ctk.CTkLabel(
            sub_frame,
            text=subtext,
            font=("Segoe UI", 12),
            text_color=("#666666", "#999999"),
            anchor="w"
        )
        subtext_label.pack(side="left", fill="x", expand=True)
        
        return frame
    
    def _create_chart(self, parent, title: str, chart_id: str) -> ctk.CTkFrame:
        """
        Crée un cadre pour un graphique.
        
        Args:
            parent: Widget parent
            title: Titre du graphique
            chart_id: Identifiant unique du graphique
            
        Returns:
            Le frame du graphique
        """
        frame = ctk.CTkFrame(
            parent,
            corner_radius=10,
            border_width=1,
            border_color=("#e0e0e0", "#333333")
        )
        
        # En-tête
        header = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 14, "bold"),
            anchor="w",
            padx=15,
            pady=12
        )
        header.pack(fill="x")
        
        # Zone du graphique (simulée)
        chart = ctk.CTkLabel(
            frame,
            text=f"[{chart_id}] Graphique en cours de chargement...",
            corner_radius=8,
            fg_color=("#f8f9fa", "#252525"),
            height=200
        )
        chart.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        return frame
    
    def _add_activity(self, icon: str, title: str, desc: str, time: str, index: int):
        """
        Ajoute une activité à la liste.
        
        Args:
            icon: Icône de l'activité
            title: Titre de l'activité
            desc: Description de l'activité
            time: Temps écoulé
            index: Position dans la liste
        """
        # Créer un cadre pour l'activité
        activity_frame = ctk.CTkFrame(
            self.activities_list,
            fg_color=("#f8f9fa", "#252525") if index % 2 == 0 else "transparent",
            corner_radius=8
        )
        activity_frame.pack(fill="x", pady=2)
        
        # Conteneur principal
        container = ctk.CTkFrame(activity_frame, fg_color="transparent")
        container.pack(fill="x", padx=10, pady=8)
        
        # Icône
        icon_label = ctk.CTkLabel(
            container,
            text=icon,
            font=("Arial", 16),
            width=30,
            anchor="center"
        )
        icon_label.pack(side="left")
        
        # Contenu
        content_frame = ctk.CTkFrame(container, fg_color="transparent")
        content_frame.pack(side="left", fill="x", expand=True)
        
        # Titre
        title_label = ctk.CTkLabel(
            content_frame,
            text=title,
            font=("Segoe UI", 13, "bold"),
            anchor="w"
        )
        title_label.pack(fill="x")
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=desc,
            font=("Segoe UI", 12),
            text_color=("#666666", "#999999"),
            anchor="w"
        )
        desc_label.pack(fill="x")
        
        # Temps
        time_label = ctk.CTkLabel(
            container,
            text=time,
            font=("Segoe UI", 11),
            text_color=("#999999", "#666666"),
            anchor="e"
        )
        time_label.pack(side="right")


if __name__ == "__main__":
    # Exemple d'utilisation
    root = ctk.CTk()
    root.title("Tableau de bord - UGANC Stock")
    root.geometry("1000x800")
    
    # Créer l'écran du tableau de bord
    dashboard = DashboardScreen(root)
    dashboard.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Démarrer la boucle principale
    root.mainloop()
