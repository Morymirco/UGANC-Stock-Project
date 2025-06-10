# core/auth_manager.py
import bcrypt
from datetime import datetime
from database.db import Database
from dataclasses import dataclass

class AuthManager:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        
    def get_connection(self):
        """Retourne une connexion à la base de données"""
        return self.db.get_connection()
    
    def hash_password(self, password):
        """Hache un mot de passe en utilisant bcrypt"""
        # Génère un sel aléatoire et hache le mot de passe
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')  # Stocke le hash sous forme de chaîne
    
    def verify_password(self, password, hashed_password):
        """Vérifie si un mot de passe correspond au hash stocké"""
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    
    def register_user(self, username, password, role, nom_complet):
        """Enregistre un nouvel utilisateur dans la base de données"""
        # Vérifier si l'utilisateur existe déjà
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Utilisateurs WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, "Nom d'utilisateur déjà utilisé"
            
            # Hacher le mot de passe
            hashed_password = self.hash_password(password)
            
            # Insérer le nouvel utilisateur
            try:
                cursor.execute("""
                    INSERT INTO Utilisateurs (username, password, role, nom_complet, last_login)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, hashed_password, role, nom_complet, None))
                conn.commit()
                return True, "Utilisateur créé avec succès"
            except Exception as e:
                return False, f"Erreur lors de la création de l'utilisateur: {str(e)}"
    
    def login(self, username, password):
        """Authentifie un utilisateur et met à jour son dernier login"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Utilisateurs WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if not user:
                return False, "Utilisateur non trouvé"
            
            if not self.verify_password(password, user["password"]):
                return False, "Mot de passe incorrect"
            
            # Mettre à jour le dernier login
            current_time = datetime.now()
            cursor.execute("""
                UPDATE Utilisateurs
                SET last_login = ?
                WHERE id = ?
            """, (current_time, user["id"]))
            conn.commit()
            
            # Créer un objet utilisateur pour la session
            self.current_user = {
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
                "nom_complet": user["nom_complet"],
                "last_login": current_time
            }
            
            return True, "Connexion réussie"
    
    def logout(self):
        """Déconnecte l'utilisateur actuel"""
        self.current_user = None
        return True, "Déconnexion réussie"
    
    def get_current_user(self):
        """Retourne l'utilisateur actuellement connecté"""
        return self.current_user
    
    def is_authenticated(self):
        """Vérifie si un utilisateur est actuellement authentifié"""
        return self.current_user is not None
    
    def has_permission(self, required_role):
        """Vérifie si l'utilisateur actuel a le rôle requis"""
        if not self.is_authenticated():
            return False
        
        # Définir la hiérarchie des rôles
        role_hierarchy = {
            "admin": 3,  # Niveau le plus élevé
            "gestionnaire": 2,
            "vendeur": 1
        }
        
        # Obtenir le niveau de l'utilisateur actuel et le niveau requis
        user_role_level = role_hierarchy.get(self.current_user["role"], 0)
        required_role_level = role_hierarchy.get(required_role, 0)
        
        # Un rôle supérieur a accès à toutes les fonctionnalités des rôles inférieurs
        return user_role_level >= required_role_level
    
    def list_users(self):
        """Liste tous les utilisateurs (accessible uniquement par l'admin)"""
        if not self.has_permission("admin"):
            return False, "Permission refusée"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Utilisateurs")
            return True, cursor.fetchall()
    
    def update_user(self, user_id, role=None, nom_complet=None):
        """Met à jour les informations d'un utilisateur (admin uniquement)"""
        if not self.has_permission("admin"):
            return False, "Permission refusée"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Construire la requête dynamiquement en fonction des champs fournis
            update_fields = []
            params = []
            
            if role:
                update_fields.append("role = ?")
                params.append(role)
            
            if nom_complet:
                update_fields.append("nom_complet = ?")
                params.append(nom_complet)
            
            if not update_fields:
                return False, "Aucun champ à mettre à jour"
            
            # Ajouter l'ID utilisateur aux paramètres
            params.append(user_id)
            
            query = f"UPDATE Utilisateurs SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()
            
            return True, "Utilisateur mis à jour avec succès"
    
    def change_password(self, user_id, old_password, new_password):
        """Change le mot de passe d'un utilisateur"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Vérifier si l'utilisateur est admin ou s'il change son propre mot de passe
            is_admin = self.has_permission("admin")
            is_own_account = self.is_authenticated() and self.current_user["id"] == user_id
            
            if not (is_admin or is_own_account):
                return False, "Permission refusée"
            
            # Vérifier l'ancien mot de passe
            cursor.execute("SELECT password FROM Utilisateurs WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            
            if not user:
                return False, "Utilisateur non trouvé"
            
            # Si ce n'est pas un admin, vérifier l'ancien mot de passe
            if not is_admin and not self.verify_password(old_password, user["password"]):
                return False, "Ancien mot de passe incorrect"
            
            # Mettre à jour le mot de passe
            hashed_password = self.hash_password(new_password)
            cursor.execute("""
                UPDATE Utilisateurs
                SET password = ?
                WHERE id = ?
            """, (hashed_password, user_id))
            conn.commit()
            
            return True, "Mot de passe changé avec succès"
    
    def delete_user(self, user_id):
        """Supprime un utilisateur (admin uniquement)"""
        if not self.has_permission("admin"):
            return False, "Permission refusée"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Utilisateurs WHERE id = ?", (user_id,))
            conn.commit()
            
            return True, "Utilisateur supprimé avec succès"
    
    def create_admin_if_not_exists(self):
        """Crée un compte administrateur par défaut s'il n'existe pas déjà"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM Utilisateurs WHERE role = 'admin'")
            result = cursor.fetchone()
            
            if result and result["count"] == 0:
                # Créer un admin par défaut
                default_admin = "admin"
                default_password = "admin123"  # À changer lors de la première connexion
                hashed_password = self.hash_password(default_password)
                
                cursor.execute("""
                    INSERT INTO Utilisateurs (username, password, role, nom_complet)
                    VALUES (?, ?, ?, ?)
                """, (default_admin, hashed_password, "admin", "Administrateur"))
                conn.commit()
                return True, "Compte administrateur par défaut créé"
            
            return False, "Des comptes administrateur existent déjà"
