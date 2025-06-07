# ui/user_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from auth_manager import AuthManager

class UserManagementUI:
    def __init__(self, parent, auth_manager):
        """
        Interface de gestion des utilisateurs
        
        Args:
            parent: La fenêtre parente
            auth_manager: L'instance du gestionnaire d'authentification
        """
        self.parent = parent
        self.auth_manager = auth_manager
        
        # Vérifier si l'utilisateur a les droits d'administration
        if not self.auth_manager.has_permission("admin"):
            messagebox.showerror("Erreur", "Vous n'avez pas les droits pour accéder à cette fonctionnalité")
            return
        
        # Créer une nouvelle fenêtre
        self.window = tk.Toplevel(parent)
        self.window.title("Gestion des utilisateurs")
        self.window.geometry("800x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrer la fenêtre
        self.center_window()
        
        # Créer les widgets
        self.create_widgets()
        
        # Charger les utilisateurs
        self.load_users()
    
    def center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Crée les widgets de l'interface"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Gestion des utilisateurs", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les boutons d'action
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(action_frame, text="Ajouter un utilisateur", command=self.show_add_user_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Modifier", command=self.show_edit_user_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Supprimer", command=self.delete_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Rafraîchir", command=self.load_users).pack(side=tk.LEFT, padx=5)
        
        # Frame pour la liste des utilisateurs
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Créer un Treeview pour afficher les utilisateurs
        columns = ("id", "username", "role", "nom_complet", "last_login")
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Définir les en-têtes de colonnes
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("username", text="Nom d'utilisateur")
        self.users_tree.heading("role", text="Rôle")
        self.users_tree.heading("nom_complet", text="Nom complet")
        self.users_tree.heading("last_login", text="Dernière connexion")
        
        # Définir les largeurs de colonnes
        self.users_tree.column("id", width=50)
        self.users_tree.column("username", width=150)
        self.users_tree.column("role", width=100)
        self.users_tree.column("nom_complet", width=200)
        self.users_tree.column("last_login", width=200)
        
        # Ajouter une barre de défilement
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.users_tree.yview)
        self.users_tree.configure(yscroll=scrollbar.set)
        
        # Placer le Treeview et la barre de défilement
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Ajouter un événement de double-clic pour modifier un utilisateur
        self.users_tree.bind("<Double-1>", lambda event: self.show_edit_user_dialog())
    
    def load_users(self):
        """Charge la liste des utilisateurs depuis la base de données"""
        # Effacer les données existantes
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        # Récupérer la liste des utilisateurs
        success, users = self.auth_manager.list_users()
        
        if not success:
            messagebox.showerror("Erreur", users)  # Dans ce cas, users contient le message d'erreur
            return
        
        # Ajouter les utilisateurs au Treeview
        for user in users:
            # Formater la date de dernière connexion
            last_login = user["last_login"] if user["last_login"] else "Jamais"
            
            # Ajouter l'utilisateur au Treeview
            self.users_tree.insert("", tk.END, values=(
                user["id"],
                user["username"],
                user["role"],
                user["nom_complet"],
                last_login
            ))
    
    def show_add_user_dialog(self):
        """Affiche la boîte de dialogue pour ajouter un utilisateur"""
        dialog = tk.Toplevel(self.window)
        dialog.title("Ajouter un utilisateur")
        dialog.geometry("400x300")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Centrer la boîte de dialogue
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text="Ajouter un utilisateur", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les champs de saisie
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Nom d'utilisateur
        username_label = ttk.Label(input_frame, text="Nom d'utilisateur:")
        username_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        username_entry = ttk.Entry(input_frame, width=30)
        username_entry.grid(row=0, column=1, pady=5)
        
        # Mot de passe
        password_label = ttk.Label(input_frame, text="Mot de passe:")
        password_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        password_entry = ttk.Entry(input_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        # Nom complet
        fullname_label = ttk.Label(input_frame, text="Nom complet:")
        fullname_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        fullname_entry = ttk.Entry(input_frame, width=30)
        fullname_entry.grid(row=2, column=1, pady=5)
        
        # Rôle
        role_label = ttk.Label(input_frame, text="Rôle:")
        role_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        role_combobox = ttk.Combobox(input_frame, width=27, values=["admin", "gestionnaire", "vendeur"])
        role_combobox.grid(row=3, column=1, pady=5)
        role_combobox.current(2)  # Par défaut "vendeur"
        
        # Bouton d'enregistrement
        def register():
            username = username_entry.get()
            password = password_entry.get()
            fullname = fullname_entry.get()
            role = role_combobox.get()
            
            if not username or not password or not fullname or not role:
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
                return
            
            success, message = self.auth_manager.register_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("Succès", message)
                dialog.destroy()
                self.load_users()  # Rafraîchir la liste des utilisateurs
            else:
                messagebox.showerror("Erreur", message)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Enregistrer", command=register).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annuler", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_edit_user_dialog(self):
        """Affiche la boîte de dialogue pour modifier un utilisateur"""
        # Récupérer l'élément sélectionné
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un utilisateur à modifier")
            return
        
        # Récupérer les données de l'utilisateur sélectionné
        user_data = self.users_tree.item(selected_item[0], "values")
        user_id = user_data[0]
        username = user_data[1]
        current_role = user_data[2]
        current_fullname = user_data[3]
        
        # Créer la boîte de dialogue
        dialog = tk.Toplevel(self.window)
        dialog.title(f"Modifier l'utilisateur: {username}")
        dialog.geometry("400x350")
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Centrer la boîte de dialogue
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        title_label = ttk.Label(main_frame, text=f"Modifier l'utilisateur: {username}", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Frame pour les champs de saisie
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # Nom complet
        fullname_label = ttk.Label(input_frame, text="Nom complet:")
        fullname_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        fullname_entry = ttk.Entry(input_frame, width=30)
        fullname_entry.grid(row=0, column=1, pady=5)
        fullname_entry.insert(0, current_fullname)
        
        # Rôle
        role_label = ttk.Label(input_frame, text="Rôle:")
        role_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        role_combobox = ttk.Combobox(input_frame, width=27, values=["admin", "gestionnaire", "vendeur"])
        role_combobox.grid(row=1, column=1, pady=5)
        
        # Sélectionner le rôle actuel
        if current_role == "admin":
            role_combobox.current(0)
        elif current_role == "gestionnaire":
            role_combobox.current(1)
        else:
            role_combobox.current(2)
        
        # Séparateur
        ttk.Separator(input_frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        # Changer le mot de passe
        password_label = ttk.Label(input_frame, text="Nouveau mot de passe:")
        password_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        password_entry = ttk.Entry(input_frame, width=30, show="*")
        password_entry.grid(row=3, column=1, pady=5)
        
        confirm_label = ttk.Label(input_frame, text="Confirmer mot de passe:")
        confirm_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        confirm_entry = ttk.Entry(input_frame, width=30, show="*")
        confirm_entry.grid(row=4, column=1, pady=5)
        
        # Boutons d'action
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def update_user():
            # Mettre à jour les informations de l'utilisateur
            fullname = fullname_entry.get()
            role = role_combobox.get()
            
            if not fullname or not role:
                messagebox.showerror("Erreur", "Veuillez remplir le nom complet et le rôle")
                return
            
            # Mettre à jour les informations de base
            success, message = self.auth_manager.update_user(user_id, role, fullname)
            if not success:
                messagebox.showerror("Erreur", message)
                return
            
            # Vérifier si un nouveau mot de passe a été saisi
            new_password = password_entry.get()
            confirm_password = confirm_entry.get()
            
            if new_password:
                if new_password != confirm_password:
                    messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
                    return
                
                # Mettre à jour le mot de passe (en tant qu'admin, pas besoin de l'ancien mot de passe)
                success, message = self.auth_manager.change_password(user_id, "", new_password)
                if not success:
                    messagebox.showerror("Erreur", message)
                    return
            
            messagebox.showinfo("Succès", "Utilisateur mis à jour avec succès")
            dialog.destroy()
            self.load_users()  # Rafraîchir la liste des utilisateurs
        
        ttk.Button(button_frame, text="Mettre à jour", command=update_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Annuler", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_user(self):
        """Supprime l'utilisateur sélectionné"""
        # Récupérer l'élément sélectionné
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un utilisateur à supprimer")
            return
        
        # Récupérer les données de l'utilisateur sélectionné
        user_data = self.users_tree.item(selected_item[0], "values")
        user_id = user_data[0]
        username = user_data[1]
        
        # Demander confirmation
        confirm = messagebox.askyesno(
            "Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur '{username}' ?\nCette action est irréversible."
        )
        
        if not confirm:
            return
        
        # Supprimer l'utilisateur
        success, message = self.auth_manager.delete_user(user_id)
        if success:
            messagebox.showinfo("Succès", message)
            self.load_users()  # Rafraîchir la liste des utilisateurs
        else:
            messagebox.showerror("Erreur", message)
