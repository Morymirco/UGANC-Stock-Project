# ui/user_management.py
import tkinter as tk
from tkinter import ttk, messagebox
from core.auth_manager import AuthManager

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
            messagebox.showerror("❌ Erreur", "Vous n'avez pas les droits pour accéder à cette fonctionnalité")
            return
        
        # Créer une nouvelle fenêtre
        self.window = tk.Toplevel(parent)
        self.window.title("Gestion des utilisateurs")
        self.window.geometry("1000x650")
        self.window.configure(bg='#2c3e50')
        self.window.transient(parent)
        self.window.grab_set()
        
        # Configuration des styles
        self.setup_styles()
        
        # Centrer la fenêtre
        self.center_window()
        
        # Créer les widgets
        self.create_widgets()
        
        # Charger les utilisateurs
        self.load_users()
    
    def setup_styles(self):
        """Configure les styles personnalisés pour l'interface"""
        style = ttk.Style()
        
        # Style pour les boutons d'action
        style.configure('Action.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=(12, 8))
    
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
        # Header stylisé
        header_frame = tk.Frame(self.window, bg='#1a252f', height=70)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Contenu du header
        header_content = tk.Frame(header_frame, bg='#1a252f')
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Titre avec icône
        title_frame = tk.Frame(header_content, bg='#1a252f')
        title_frame.pack(side=tk.LEFT)
        
        title_icon = tk.Label(title_frame, text="👥", font=('Arial', 20), 
                             bg='#1a252f', fg='#ecf0f1')
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(title_frame, text="Gestion des Utilisateurs", 
                              font=('Arial', 16, 'bold'), bg='#1a252f', fg='#ecf0f1')
        title_label.pack(side=tk.LEFT)
        
        # Bouton fermer
        close_btn = tk.Button(header_content, text="← Retour", 
                             command=self.window.destroy, font=('Arial', 10),
                             bg='#34495e', fg='#ecf0f1', borderwidth=0,
                             padx=15, pady=8, cursor='hand2')
        close_btn.pack(side=tk.RIGHT)
        
        # Container principal
        main_container = tk.Frame(self.window, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Section des actions
        actions_frame = tk.Frame(main_container, bg='#34495e', relief='solid', bd=1)
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        actions_header = tk.Frame(actions_frame, bg='#1a252f')
        actions_header.pack(fill=tk.X)
        
        actions_title = tk.Label(actions_header, text="🚀 Actions sur les utilisateurs", 
                                font=('Arial', 14, 'bold'), bg='#1a252f', fg='#ecf0f1')
        actions_title.pack(pady=10)
        
        # Ligne de séparation
        separator = tk.Frame(actions_frame, bg='#7f8c8d', height=1)
        separator.pack(fill=tk.X)
        
        actions_content = tk.Frame(actions_frame, bg='#34495e')
        actions_content.pack(fill=tk.X, padx=20, pady=15)
        
        # Boutons d'action stylisés
        buttons_row = tk.Frame(actions_content, bg='#34495e')
        buttons_row.pack(fill=tk.X)
        
        tk.Button(buttons_row, text="➕ Ajouter un utilisateur", command=self.show_add_user_dialog,
                 font=('Arial', 10, 'bold'), bg='#27ae60', fg='white', 
                 borderwidth=0, padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(buttons_row, text="✏️ Modifier", command=self.show_edit_user_dialog,
                 font=('Arial', 10, 'bold'), bg='#3498db', fg='white', 
                 borderwidth=0, padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(buttons_row, text="🗑️ Supprimer", command=self.delete_user,
                 font=('Arial', 10, 'bold'), bg='#e74c3c', fg='white', 
                 borderwidth=0, padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(buttons_row, text="🔄 Rafraîchir", command=self.load_users,
                 font=('Arial', 10, 'bold'), bg='#95a5a6', fg='white', 
                 borderwidth=0, padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT)
        
        # Section du tableau
        table_frame = tk.Frame(main_container, bg='#34495e', relief='solid', bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        table_header = tk.Frame(table_frame, bg='#1a252f')
        table_header.pack(fill=tk.X)
        
        table_title = tk.Label(table_header, text="👥 Liste des utilisateurs", 
                              font=('Arial', 14, 'bold'), bg='#1a252f', fg='#ecf0f1')
        table_title.pack(pady=10)
        
        # Ligne de séparation
        separator2 = tk.Frame(table_frame, bg='#7f8c8d', height=1)
        separator2.pack(fill=tk.X)
        
        # Frame pour la liste des utilisateurs
        list_frame = tk.Frame(table_frame, bg='#34495e')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Créer un Treeview pour afficher les utilisateurs
        columns = ("id", "username", "role", "nom_complet", "last_login")
        self.users_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Définir les en-têtes de colonnes avec icônes
        headers = [
            ("id", "🆔 ID"),
            ("username", "👤 Nom d'utilisateur"),
            ("role", "🎭 Rôle"),
            ("nom_complet", "📝 Nom complet"),
            ("last_login", "🕐 Dernière connexion")
        ]
        
        for col, header_text in headers:
            self.users_tree.heading(col, text=header_text)
        
        # Définir les largeurs de colonnes
        self.users_tree.column("id", width=60)
        self.users_tree.column("username", width=150)
        self.users_tree.column("role", width=120)
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
            messagebox.showerror("❌ Erreur", users)  # Dans ce cas, users contient le message d'erreur
            return
        
        # Ajouter les utilisateurs au Treeview
        for user in users:
            # Formater la date de dernière connexion
            last_login = user["last_login"] if user["last_login"] else "❌ Jamais"
            
            # Déterminer le tag selon le rôle
            role = user["role"]
            if role == "admin":
                tags = ('admin',)
            elif role == "gestionnaire":
                tags = ('gestionnaire',)
            else:
                tags = ('vendeur',)
            
            # Ajouter l'utilisateur au Treeview
            self.users_tree.insert("", tk.END, values=(
                user["id"],
                user["username"],
                f"🔧 {role}" if role == "admin" else f"⚙️ {role}" if role == "gestionnaire" else f"🛒 {role}",
                user["nom_complet"],
                last_login
            ), tags=tags)
        
        # Configuration des couleurs pour les tags (dark theme)
        self.users_tree.tag_configure('admin', background='#8b1538', foreground='white')
        self.users_tree.tag_configure('gestionnaire', background='#1c4966', foreground='white')
        self.users_tree.tag_configure('vendeur', background='#1e5128', foreground='white')
    
    def show_add_user_dialog(self):
        """Affiche la boîte de dialogue moderne pour ajouter un utilisateur"""
        dialog = tk.Toplevel(self.window)
        dialog.title("➕ Ajouter un utilisateur")
        dialog.geometry("500x400")
        dialog.configure(bg='#2c3e50')
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Centrer la boîte de dialogue
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg='#27ae60', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#27ae60')
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text="➕ Ajouter un nouvel utilisateur", 
                              font=('Arial', 14, 'bold'), bg='#27ae60', fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Contenu principal
        main_frame = tk.Frame(dialog, bg='#34495e', relief='solid', bd=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content_frame = tk.Frame(main_frame, bg='#34495e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Frame pour les champs de saisie
        input_frame = tk.Frame(content_frame, bg='#34495e')
        input_frame.pack(fill=tk.X, pady=10)
        
        # Style moderne pour les champs
        fields = [
            ("👤 Nom d'utilisateur:", 0),
            ("🔒 Mot de passe:", 1),
            ("📝 Nom complet:", 2),
            ("🎭 Rôle:", 3)
        ]
        
        entries = {}
        
        for label_text, row in fields:
            label = tk.Label(input_frame, text=label_text, 
                           font=('Arial', 11, 'bold'), bg='#34495e', fg='#ecf0f1')
            label.grid(row=row, column=0, sticky=tk.W, pady=8, padx=(0, 10))
            
            if "Rôle" in label_text:
                entry = ttk.Combobox(input_frame, width=25, values=["admin", "gestionnaire", "vendeur"], state="readonly")
                entry.current(2)  # Par défaut "vendeur"
            else:
                entry = tk.Entry(input_frame, font=('Arial', 11), width=28, 
                               relief='solid', bd=1, bg='#95a5a6', fg='#2c3e50')
                if "Mot de passe" in label_text:
                    entry.config(show="*")
            
            entry.grid(row=row, column=1, pady=8)
            entries[row] = entry
        
        # Boutons
        button_frame = tk.Frame(content_frame, bg='#34495e')
        button_frame.pack(pady=20)
        
        def register():
            username = entries[0].get().strip()
            password = entries[1].get()
            fullname = entries[2].get().strip()
            role = entries[3].get()
            
            if not username or not password or not fullname or not role:
                messagebox.showerror("❌ Erreur", "Veuillez remplir tous les champs")
                return
            
            success, message = self.auth_manager.register_user(username, password, role, fullname)
            if success:
                messagebox.showinfo("✅ Succès", message)
                dialog.destroy()
                self.load_users()  # Rafraîchir la liste des utilisateurs
            else:
                messagebox.showerror("❌ Erreur", message)
        
        tk.Button(button_frame, text="✅ Enregistrer", command=register,
                 font=('Arial', 11, 'bold'), bg='#27ae60', fg='white', 
                 borderwidth=0, padx=20, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="❌ Annuler", command=dialog.destroy,
                 font=('Arial', 11), bg='#95a5a6', fg='white', 
                 borderwidth=0, padx=20, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=10)
        
        # Focus sur le premier champ
        entries[0].focus()
    
    def show_edit_user_dialog(self):
        """Affiche la boîte de dialogue moderne pour modifier un utilisateur"""
        # Récupérer l'élément sélectionné
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("⚠️ Avertissement", "Veuillez sélectionner un utilisateur à modifier")
            return
        
        # Récupérer les données de l'utilisateur sélectionné
        user_data = self.users_tree.item(selected_item[0], "values")
        user_id = user_data[0]
        username = user_data[1]
        current_role = user_data[2].split()[1]  # Enlever l'emoji
        current_fullname = user_data[3]
        
        # Créer la boîte de dialogue
        dialog = tk.Toplevel(self.window)
        dialog.title("✏️ Modifier un utilisateur")
        dialog.geometry("500x450")
        dialog.configure(bg='#2c3e50')
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Centrer la boîte de dialogue
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(dialog, bg='#3498db', height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#3498db')
        header_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        title_label = tk.Label(header_content, text=f"✏️ Modifier l'utilisateur: {username}", 
                              font=('Arial', 14, 'bold'), bg='#3498db', fg='white')
        title_label.pack(side=tk.LEFT)
        
        # Contenu principal
        main_frame = tk.Frame(dialog, bg='#34495e', relief='solid', bd=1)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content_frame = tk.Frame(main_frame, bg='#34495e')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Frame pour les champs de saisie
        input_frame = tk.Frame(content_frame, bg='#34495e')
        input_frame.pack(fill=tk.X, pady=10)
        
        # Nom complet
        fullname_label = tk.Label(input_frame, text="📝 Nom complet:",
                                 font=('Arial', 11, 'bold'), bg='#34495e', fg='#ecf0f1')
        fullname_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        fullname_entry = tk.Entry(input_frame, width=30, font=('Arial', 11),
                                 bg='#95a5a6', fg='#2c3e50', relief='solid', bd=1)
        fullname_entry.grid(row=0, column=1, pady=5)
        fullname_entry.insert(0, current_fullname)
        
        # Rôle
        role_label = tk.Label(input_frame, text="🎭 Rôle:",
                             font=('Arial', 11, 'bold'), bg='#34495e', fg='#ecf0f1')
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
        sep_frame = tk.Frame(input_frame, bg='#7f8c8d', height=2)
        sep_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=15)
        
        # Changer le mot de passe
        password_label = tk.Label(input_frame, text="🔒 Nouveau mot de passe:",
                                 font=('Arial', 11, 'bold'), bg='#34495e', fg='#ecf0f1')
        password_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        password_entry = tk.Entry(input_frame, width=30, show="*", font=('Arial', 11),
                                 bg='#95a5a6', fg='#2c3e50', relief='solid', bd=1)
        password_entry.grid(row=3, column=1, pady=5)
        
        confirm_label = tk.Label(input_frame, text="🔒 Confirmer mot de passe:",
                                font=('Arial', 11, 'bold'), bg='#34495e', fg='#ecf0f1')
        confirm_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        confirm_entry = tk.Entry(input_frame, width=30, show="*", font=('Arial', 11),
                                bg='#95a5a6', fg='#2c3e50', relief='solid', bd=1)
        confirm_entry.grid(row=4, column=1, pady=5)
        
        # Info text
        info_label = tk.Label(content_frame, text="💡 Laissez vide pour conserver le mot de passe actuel",
                             font=('Arial', 9, 'italic'), bg='#34495e', fg='#bdc3c7')
        info_label.pack(pady=5)
        
        # Boutons d'action
        button_frame = tk.Frame(content_frame, bg='#34495e')
        button_frame.pack(fill=tk.X, pady=20)
        
        def update_user():
            # Mettre à jour les informations de l'utilisateur
            fullname = fullname_entry.get().strip()
            role = role_combobox.get()
            
            if not fullname or not role:
                messagebox.showerror("❌ Erreur", "Veuillez remplir le nom complet et le rôle")
                return
            
            # Mettre à jour les informations de base
            success, message = self.auth_manager.update_user(user_id, role, fullname)
            if not success:
                messagebox.showerror("❌ Erreur", message)
                return
            
            # Vérifier si un nouveau mot de passe a été saisi
            new_password = password_entry.get()
            confirm_password = confirm_entry.get()
            
            if new_password:
                if new_password != confirm_password:
                    messagebox.showerror("❌ Erreur", "Les mots de passe ne correspondent pas")
                    return
                
                # Mettre à jour le mot de passe (en tant qu'admin, pas besoin de l'ancien mot de passe)
                success, message = self.auth_manager.change_password(user_id, "", new_password)
                if not success:
                    messagebox.showerror("❌ Erreur", message)
                    return
            
            messagebox.showinfo("✅ Succès", "Utilisateur mis à jour avec succès")
            dialog.destroy()
            self.load_users()  # Rafraîchir la liste des utilisateurs
        
        tk.Button(button_frame, text="✅ Mettre à jour", command=update_user,
                 font=('Arial', 11, 'bold'), bg='#3498db', fg='white',
                 borderwidth=0, padx=20, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="❌ Annuler", command=dialog.destroy,
                 font=('Arial', 11), bg='#95a5a6', fg='white',
                 borderwidth=0, padx=20, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=10)
    
    def delete_user(self):
        """Supprime l'utilisateur sélectionné"""
        # Récupérer l'élément sélectionné
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("⚠️ Avertissement", "Veuillez sélectionner un utilisateur à supprimer")
            return
        
        # Récupérer les données de l'utilisateur sélectionné
        user_data = self.users_tree.item(selected_item[0], "values")
        user_id = user_data[0]
        username = user_data[1]
        
        # Demander confirmation
        confirm = messagebox.askyesno(
            "⚠️ Confirmation", 
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur '{username}' ?\n\n"
            f"⚠️ Cette action est irréversible."
        )
        
        if not confirm:
            return
        
        # Supprimer l'utilisateur
        success, message = self.auth_manager.delete_user(user_id)
        if success:
            messagebox.showinfo("✅ Succès", message)
            self.load_users()  # Rafraîchir la liste des utilisateurs
        else:
            messagebox.showerror("❌ Erreur", message)
