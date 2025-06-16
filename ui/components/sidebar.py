import customtkinter as ctk
from typing import Dict, Callable, Optional

class Sidebar(ctk.CTkFrame):
    """
    Professional, animated, collapsible sidebar for UGANC Stock.
    """
    
    # Style constants
    COLORS = {
        "light": {
            "bg": "#f7fafc",
            "sidebar_bg": "#ffffff",
            "hover": "#edf2f7",
            "active": "#e2e8ff",
            "gradient_start": "#4c51bf",
            "gradient_end": "#7f9cf5",
            "text": "#2d3748",
            "primary": "#4c51bf",
            "tooltip_bg": "#2d3748",
            "tooltip_text": "#ffffff",
            "logout_border": "#e53e3e",
            "logout_text": "#e53e3e",
            "logout_hover": "#fed7d7"
        },
        "dark": {
            "bg": "#1a202c",
            "sidebar_bg": "#2d3748",
            "hover": "#4a5568",
            "active": "#3c4a6b",
            "gradient_start": "#5a67d8",
            "gradient_end": "#a3bffa",
            "text": "#e2e8f0",
            "primary": "#5a67d8",
            "tooltip_bg": "#e2e8f0",
            "tooltip_text": "#2d3748",
            "logout_border": "#f56565",
            "logout_text": "#f56565",
            "logout_hover": "#742a2a"
        }
    }
    FONTS = {
        "logo": ("Inter", 20),
        "app_name": ("Inter", 15, "bold"),
        "button": ("Inter", 13),
        "button_active": ("Inter", 13, "bold"),
        "logout": ("Inter", 12, "bold"),
        "tooltip": ("Inter", 11)
    }
    SIZES = {
        "full_width": 220,
        "collapsed_width": 60,
        "header_height": 60,
        "button_height": 40,
        "footer_height": 60,
        "indicator_width": 3,
        "animation_steps": 10,
        "animation_delay": 20
    }
    
    def __init__(self, parent, on_button_click: Callable[[str], None] = None, **kwargs):
        """
        Initialize the sidebar.
        
        Args:
            parent: Parent widget
            on_button_click: Callback for button clicks
            **kwargs: Additional arguments for CTkFrame
        """
        super().__init__(parent, fg_color=(self.COLORS["light"]["sidebar_bg"], 
                                         self.COLORS["dark"]["sidebar_bg"]), 
                        corner_radius=0, width=self.SIZES["full_width"], **kwargs)
        print("DEBUG: Initializing Sidebar")
        
        self.on_button_click = on_button_click
        self.buttons: Dict[str, Dict] = {}
        self.active_button: Optional[str] = None
        self.is_collapsed = False
        self.tooltip_window = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Create widgets
        self._create_widgets()
    
    def _create_widgets(self):
        """Create sidebar widgets."""
        print("DEBUG: Creating widgets")
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=self.SIZES["header_height"])
        self.header_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        self.toggle_btn = ctk.CTkButton(
            self.header_frame,
            text="☰",
            font=self.FONTS["logo"],
            fg_color="transparent",
            hover_color=(self.COLORS["light"]["hover"], self.COLORS["dark"]["hover"]),
            text_color=(self.COLORS["light"]["primary"], self.COLORS["dark"]["primary"]),
            width=30,
            command=self._toggle_collapse
        )
        self.toggle_btn.pack(side="left")
        
        self.logo_label = ctk.CTkLabel(
            self.header_frame,
            text="📊",
            font=self.FONTS["logo"],
            text_color=(self.COLORS["light"]["primary"], self.COLORS["dark"]["primary"])
        )
        self.logo_label.pack(side="left", padx=(5, 8))
        
        self.app_name = ctk.CTkLabel(
            self.header_frame,
            text="UGANC Stock",
            font=self.FONTS["app_name"],
            text_color=(self.COLORS["light"]["text"], self.COLORS["dark"]["text"])
        )
        self.app_name.pack(side="left")
        
        # Navigation buttons
        self.buttons_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        
        menu_items = [
            ("Tableau de bord", "📊", "dashboard"),
            ("Articles", "📝", "articles"),
            ("Stocks", "📦", "stock"),
            ("Paramètres", "⚙️", "parametres")
        ]
        
        for i, (text, icon, key) in enumerate(menu_items):
            self._create_button(text, icon, key, i)
        self.buttons_frame.rowconfigure(len(menu_items), weight=1)
        
        # Footer
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=self.SIZES["footer_height"])
        self.footer_frame.grid(row=2, column=0, sticky="sew", padx=10, pady=(0, 10))
        
        self.logout_btn = ctk.CTkButton(
            self.footer_frame,
            text="Déconnexion",
            font=self.FONTS["logout"],
            fg_color="transparent",
            border_width=1,
            border_color=(self.COLORS["light"]["logout_border"], self.COLORS["dark"]["logout_border"]),
            text_color=(self.COLORS["light"]["logout_text"], self.COLORS["dark"]["logout_text"]),
            hover_color=(self.COLORS["light"]["logout_hover"], self.COLORS["dark"]["logout_hover"]),
            corner_radius=6,
            height=self.SIZES["button_height"],
            command=lambda: self._on_button_click("Déconnexion")
        )
        self.logout_btn.pack(fill="x", pady=(5, 0))
    
    def _create_button(self, text: str, icon: str, key: str, row: int):
        """
        Create a navigation button with animation support.
        
        Args:
            text: Button text
            icon: Button icon
            key: Unique button key
            row: Grid row
        """
        btn_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent", height=self.SIZES["button_height"])
        btn_frame.grid(row=row, column=0, sticky="ew", pady=3)
        btn_frame.grid_columnconfigure(1, weight=1)
        
        indicator = ctk.CTkLabel(
            btn_frame, 
            text="", 
            width=self.SIZES["indicator_width"],
            corner_radius=2,
            fg_color="transparent"
        )
        indicator.grid(row=0, column=0, sticky="ns", padx=5)
        
        btn = ctk.CTkButton(
            btn_frame,
            text=f"{icon}  {text}" if not self.is_collapsed else icon,
            font=self.FONTS["button"],
            anchor="w" if not self.is_collapsed else "center",
            fg_color="transparent",
            text_color=(self.COLORS["light"]["text"], self.COLORS["dark"]["text"]),
            hover_color=(self.COLORS["light"]["hover"], self.COLORS["dark"]["hover"]),
            corner_radius=6,
            height=self.SIZES["button_height"],
            command=lambda: self._on_button_click(text)
        )
        btn.grid(row=0, column=1, sticky="ew", padx=(0, 5))
        
        self.buttons[key] = {
            'button': btn, 
            'indicator': indicator, 
            'frame': btn_frame, 
            'text': text, 
            'row': row
        }
        
        btn.bind("<Enter>", lambda e: self._on_hover(key, True))
        btn.bind("<Leave>", lambda e: self._on_hover(key, False))
        btn.bind("<Enter>", lambda e: self._show_tooltip(btn, text), add="+")
        btn.bind("<Leave>", lambda e: self._hide_tooltip(), add="+")
    
    def _toggle_collapse(self):
        """Toggle sidebar collapse state with animation."""
        print("DEBUG: Toggling sidebar collapse")
        self.is_collapsed = not self.is_collapsed
        target_width = self.SIZES["collapsed_width"] if self.is_collapsed else self.SIZES["full_width"]
        
        # Animate width
        self._animate_width(target_width)
        
        # Update button appearance
        for key, elements in self.buttons.items():
            btn = elements['button']
            text = elements['text']
            btn.configure(
                text=icon if self.is_collapsed else f"{icon}  {text}",
                anchor="center" if self.is_collapsed else "w"
            )
        
        # Update app name and logout button
        self.app_name.pack_forget() if self.is_collapsed else self.app_name.pack(side="left")
        self.logout_btn.configure(
            text="🚪" if self.is_collapsed else "Déconnexion",
            anchor="center" if self.is_collapsed else "w"
        )
    
    def _animate_width(self, target_width: int):
        """Animate sidebar width transition."""
        current_width = self.winfo_width() or self.SIZES["full_width"]  # Fallback if not rendered
        if current_width == target_width:
            return
        
        step = (target_width - current_width) / self.SIZES["animation_steps"]
        
        def animate(step_count=0):
            if step_count >= self.SIZES["animation_steps"]:
                self.configure(width=target_width)
                self.buttons_frame.configure(width=target_width - 10)
                print(f"DEBUG: Animation width completed at {target_width}px")
                return
            
            new_width = current_width + step * (step_count + 1)
            self.configure(width=int(new_width))
            self.buttons_frame.configure(width=int(new_width - 10))
            self.after(self.SIZES["animation_delay"], lambda: animate(step_count + 1))
        
        print(f"DEBUG: Animating width from {current_width} to {target_width}")
        animate()
    
    def _show_tooltip(self, widget, text: str):
        """Show tooltip for a button in collapsed mode."""
        if not self.is_collapsed:
            return
        self._hide_tooltip()
        x, y = widget.winfo_rootx() + widget.winfo_width() + 5, widget.winfo_rooty() + 10
        self.tooltip_window = ctk.CTkToplevel(self)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(
            self.tooltip_window,
            text=text,
            font=self.FONTS["tooltip"],
            fg_color=(self.COLORS["light"]["tooltip_bg"], self.COLORS["dark"]["tooltip_bg"]),
            text_color=(self.COLORS["light"]["tooltip_text"], self.COLORS["dark"]["tooltip_text"]),
            corner_radius=4,
            padx=8,
            pady=4
        )
        label.pack()
        print(f"DEBUG: Showing tooltip for '{text}'")
    
    def _hide_tooltip(self):
        """Hide tooltip."""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None
            print("DEBUG: Hiding tooltip")
    
    def _on_button_click(self, button_name: str):
        """
        Handle button click with animation.
        
        Args:
            button_name: Name of clicked button
        """
        print(f"DEBUG: Click on '{button_name}'")
        key = button_name.lower()
        if key in self.buttons or button_name == "Déconnexion":
            self.set_active_button(key)
            if self.on_button_click:
                print(f"DEBUG: Calling on_button_click with '{button_name}'")
                self.on_button_click(button_name)
            else:
                print("DEBUG: No callback defined")
        else:
            print(f"ERROR: Key '{key}' not found")
    
    def _on_hover(self, button_key: str, is_hovered: bool):
        """
        Handle hover effect.
        
        Args:
            button_key: Button key
            is_hovered: Hover state
        """
        if button_key not in self.buttons:
            print(f"DEBUG: Key '{button_key}' not found for hover")
            return
        print(f"DEBUG: Hover {'on' if is_hovered else 'off'} for '{button_key}'")
        
        btn = self.buttons[button_key]['button']
        indicator = self.buttons[button_key]['indicator']
        
        if is_hovered:
            btn.configure(fg_color=(self.COLORS["light"]["hover"], self.COLORS["dark"]["hover"]))
            indicator.configure(fg_color=(self.COLORS["light"]["primary"], self.COLORS["dark"]["primary"]))
        elif button_key != self.active_button:
            btn.configure(fg_color="transparent")
            indicator.configure(fg_color="transparent")
    
    def _animate_indicator(self, button_key: str):
        """
        Animate selection indicator with smooth transition.
        
        Args:
            button_key: Selected button key
        """
        if button_key not in self.buttons:
            print(f"DEBUG: Key '{button_key}' not found for animation")
            return
        print(f"DEBUG: Animating indicator for '{button_key}'")
        
        # Reset all buttons
        for key, elements in self.buttons.items():
            elements['indicator'].configure(fg_color="transparent")
            elements['button'].configure(
                font=self.FONTS["button"],
                text_color=(self.COLORS["light"]["text"], self.COLORS["dark"]["text"]),
                fg_color="transparent"
            )
        
        # Animate active button
        indicator = self.buttons[button_key]['indicator']
        btn = self.buttons[button_key]['button']
        indicator.configure(fg_color=(self.COLORS["light"]["primary"], self.COLORS["dark"]["primary"]))
        btn.configure(
            font=self.FONTS["button_active"],
            text_color=(self.COLORS["light"]["primary"], self.COLORS["dark"]["primary"]),
            fg_color=(self.COLORS["light"]["active"], self.COLORS["dark"]["active"])
        )
    
    def set_active_button(self, button_key: str):
        """
        Set active button with animation.
        
        Args:
            button_key: Key of active button
        """
        print(f"DEBUG: Setting active button: '{button_key}'")
        self.active_button = button_key if button_key in self.buttons else None
        if self.active_button:
            self._animate_indicator(self.active_button)
            for key, elements in self.buttons.items():
                btn = elements['button']
                if key == self.active_button:
                    btn.configure(
                        fg_color=(self.COLORS["light"]["active"], self.COLORS["dark"]["active"]),
                        hover_color=(self.COLORS["light"]["active"], self.COLORS["dark"]["active"]),
                        text_color=(self.COLORS["light"]["primary"], self.COLORS["dark"]["primary"]),
                        font=self.FONTS["button_active"]
                    )
                else:
                    btn.configure(
                        fg_color="transparent",
                        hover_color=(self.COLORS["light"]["hover"], self.COLORS["dark"]["hover"]),
                        text_color=(self.COLORS["light"]["text"], self.COLORS["dark"]["text"]),
                        font=self.FONTS["button"]
                    )
    
    def get_active_button(self) -> Optional[str]:
        """Return active button."""
        print(f"DEBUG: Active button: '{self.active_button}'")
        return self.active_button
    
    def set_width(self, width: int):
        """Set sidebar width."""
        print(f"DEBUG: Setting width to {width}px")
        self.configure(width=width)
        self.buttons_frame.configure(width=width - 10)
    
    def set_theme(self, theme: str):
        """
        Change theme (light/dark).
        
        Args:
            theme: "light" or "dark"
        """
        print(f"DEBUG: Changing theme to '{theme}'")
        theme = theme.lower()
        if theme not in ["light", "dark"]:
            print(f"DEBUG: Invalid theme '{theme}', using 'light'")
            theme = "light"
        
        bg_color = self.COLORS[theme]["sidebar_bg"]
        self.configure(fg_color=bg_color)
        self.buttons_frame.configure(fg_color=bg_color)
        
        for key, elements in self.buttons.items():
            btn = elements['button']
            btn.configure(
                text_color=self.COLORS[theme]["text"],
                hover_color=self.COLORS[theme]["hover"],
                fg_color="transparent" if key != self.active_button else self.COLORS[theme]["active"]
            )
        
        self.logout_btn.configure(
            text_color=self.COLORS[theme]["logout_text"],
            hover_color=self.COLORS[theme]["logout_hover"],
            border_color=self.COLORS[theme]["logout_border"],
            fg_color="transparent"
        )
        
        self.toggle_btn.configure(
            text_color=self.COLORS[theme]["primary"],
            hover_color=self.COLORS[theme]["hover"]
        )
        
        if self.active_button:
            self.set_active_button(self.active_button)

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("300x600")
    sidebar = Sidebar(root, on_button_click=lambda x: print(f"Clicked: {x}"))
    sidebar.pack(fill="y", side="left")
    root.mainloop()