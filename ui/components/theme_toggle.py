"""
Composant de basculement de thème
"""
import customtkinter as ctk
from PIL import Image, ImageDraw
import math

class ThemeToggle(ctk.CTkButton):
    def __init__(self, master, command=None, **kwargs):
        self.size = 20
        self.light_icon = self._create_light_icon()
        self.dark_icon = self._create_dark_icon()
        
        super().__init__(
            master=master,
            text="",
            image=self.light_icon if ctk.get_appearance_mode() == "Light" else self.dark_icon,
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=("#f0f0f0", "#2d2d2d"),
            command=self._toggle_theme,
            corner_radius=15,
            **kwargs
        )
        
        self._command = command
    
    def _create_light_icon(self):
        """Crée l'icône pour le mode clair (soleil)"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Cercle du soleil
        draw.ellipse((0, 0, self.size-1, self.size-1), fill="#ffd700")
        
        # Rayons du soleil
        for i in range(8):
            angle = i * 45
            x1 = self.size//2 + int((self.size//2 - 2) * 0.7 * math.cos(math.radians(angle)))
            y1 = self.size//2 + int((self.size//2 - 2) * 0.7 * math.sin(math.radians(angle)))
            x2 = self.size//2 + int((self.size//2 + 2) * 1.5 * math.cos(math.radians(angle)))
            y2 = self.size//2 + int((self.size//2 + 2) * 1.5 * math.sin(math.radians(angle)))
            draw.line([(x1, y1), (x2, y2)], fill="#ffd700", width=2)
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(self.size, self.size))
    
    def _create_dark_icon(self):
        """Crée l'icône pour le mode sombre (lune)"""
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Cercle de la lune
        draw.ellipse((0, 0, self.size-1, self.size-1), fill="#f0f0f0")
        
        # Partie sombre pour former le croissant
        # Utilisation d'une couleur fixe pour éviter les problèmes de thème
        crescent_color = "#f0f0f0" if ctk.get_appearance_mode() == "Light" else "#000000"
        draw.ellipse((self.size//3, 0, self.size-1, self.size*2//3), fill=crescent_color)
        
        return ctk.CTkImage(light_image=img, dark_image=img, size=(self.size, self.size))
    
    def _toggle_theme(self):
        """Bascule entre les thèmes clair et sombre"""
        current_theme = ctk.get_appearance_mode().lower()
        new_theme = "dark" if current_theme == "light" else "light"
        ctk.set_appearance_mode(new_theme)
        
        # Mettre à jour l'icône
        self.configure(image=self.light_icon if new_theme == "light" else self.dark_icon)
        
        if self._command:
            self._command()
