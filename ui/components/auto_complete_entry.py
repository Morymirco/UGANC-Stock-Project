"""
Composant de champ de saisie avec autocomplétion
"""
import tkinter as tk
import customtkinter as ctk
from typing import List, Callable, Optional

class AutoCompleteEntry(ctk.CTkFrame):
    def __init__(self, 
                 master, 
                 placeholder: str = "", 
                 get_suggestions: Optional[Callable[[str], List[str]]] = None,
                 **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.get_suggestions = get_suggestions or (lambda x: [])
        self.on_select = None
        self.suggestions_visible = False
        self.current_suggestion_index = -1
        
        # Champ de saisie principal
        self.entry_var = tk.StringVar()
        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.entry_var,
            placeholder_text=placeholder,
            height=45,
            corner_radius=10,
            font=("Arial", 14)
        )
        self.entry.pack(fill=tk.X)
        
        # Frame pour les suggestions
        self.suggestions_frame = ctk.CTkScrollableFrame(
            self,
            height=0,
            fg_color=("#f0f0f0", "#2d2d2d"),
            corner_radius=5
        )
        self.suggestions_frame.pack(fill=tk.X, pady=(2, 0))
        self.suggestions_frame.pack_forget()
        
        # Liste des boutons de suggestion
        self.suggestion_buttons = []
        
        # Lier les événements
        self.entry_var.trace_add('write', self._on_text_changed)
        self.entry.bind('<Down>', self._on_arrow_key)
        self.entry.bind('<Up>', self._on_arrow_key)
        self.entry.bind('<Return>', self._on_enter)
        self.entry.bind('<Escape>', lambda e: self._hide_suggestions())
        self.entry.bind('<FocusOut>', self._on_focus_out)
    
    def _on_text_changed(self, *args):
        """Appelé lorsque le texte change"""
        self._hide_suggestions()
        text = self.entry_var.get().lower()
        
        if not text:
            return
            
        suggestions = self.get_suggestions(text)
        if suggestions:
            self._show_suggestions(suggestions)
    
    def _show_suggestions(self, suggestions: List[str]):
        """Affiche les suggestions"""
        self._clear_suggestions()
        
        for i, suggestion in enumerate(suggestions[:5]):
            btn = ctk.CTkButton(
                self.suggestions_frame,
                text=suggestion,
                anchor="w",
                fg_color="transparent",
                hover_color=("#e0e0e0", "#3d3d3d"),
                text_color=("#000000", "#ffffff"),
                command=lambda s=suggestion: self._select_suggestion(s)
            )
            btn.pack(fill=tk.X, pady=1)
            self.suggestion_buttons.append(btn)
        
        self.suggestions_frame.configure(height=min(5, len(suggestions)) * 35)
        self.suggestions_frame.pack()
        self.suggestions_visible = True
    
    def _hide_suggestions(self):
        """Cache les suggestions"""
        if self.suggestions_visible:
            self.suggestions_frame.pack_forget()
            self.suggestions_visible = False
            self.current_suggestion_index = -1
    
    def _clear_suggestions(self):
        """Vide la liste des suggestions"""
        for btn in self.suggestion_buttons:
            btn.destroy()
        self.suggestion_buttons = []
    
    def _select_suggestion(self, text: str):
        """Sélectionne une suggestion"""
        self.entry_var.set(text)
        self._hide_suggestions()
        if self.on_select:
            self.on_select(text)
    
    def _on_arrow_key(self, event):
        """Gère la navigation avec les flèches"""
        if not self.suggestions_visible:
            return
            
        if event.keysym == 'Down':
            self.current_suggestion_index = (self.current_suggestion_index + 1) % len(self.suggestion_buttons)
        elif event.keysym == 'Up':
            self.current_suggestion_index = (self.current_suggestion_index - 1) % len(self.suggestion_buttons)
        
        for i, btn in enumerate(self.suggestion_buttons):
            if i == self.current_suggestion_index:
                btn.configure(fg_color=("#e0e0e0", "#4d4d4d"))
            else:
                btn.configure(fg_color="transparent")
    
    def _on_enter(self, event):
        """Gère la touche Entrée"""
        if self.suggestions_visible and 0 <= self.current_suggestion_index < len(self.suggestion_buttons):
            self._select_suggestion(self.suggestion_buttons[self.current_suggestion_index].cget("text"))
            return "break"
    
    def _on_focus_out(self, event):
        """Gère la perte de focus"""
        if not self.suggestions_frame.winfo_ismapped():
            return
            
        x, y = self.winfo_toplevel().winfo_pointerxy()
        widget = self.winfo_containing(x, y)
        
        if widget not in [self.suggestions_frame] + self.suggestion_buttons + [self.entry]:
            self._hide_suggestions()
    
    def get(self) -> str:
        """Retourne la valeur du champ"""
        return self.entry_var.get()
    
    def set(self, value: str):
        """Définit la valeur du champ"""
        self.entry_var.set(value)
    
    def focus(self):
        """Donne le focus au champ"""
        self.entry.focus()
    
    def bind(self, sequence=None, command=None, add=None):
        """Redirige les événements vers le champ de saisie"""
        return self.entry.bind(sequence, command, add)
