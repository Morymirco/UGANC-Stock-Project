# database/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Utilisateur:
    id: int
    username: str
    password: str
    role: str
    nom_complet: str
    last_login: datetime = None

@dataclass
class Article:
    code_article: str
    designation: str
    categorie: str
    prix_achat: float
    prix_vente: float
    seuil_alerte: int

@dataclass
class Stock:
    id: int
    code_article: str
    quantite: int
    emplacement: str

@dataclass
class Mouvement:
    id: int
    type: str
    code_article: str
    quantite: int
    date_mvt: datetime
    user_id: int

@dataclass
class Fournisseur:
    id: int
    nom: str
    contact: str