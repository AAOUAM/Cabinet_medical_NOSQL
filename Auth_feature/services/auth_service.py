import bcrypt
from datetime import datetime
from bson import ObjectId
from ..Config import (DatabaseConnections)
from functools import wraps
from flask import session, request, redirect, url_for, flash

class AuthService:

    @staticmethod
    def hash_password(password):
        """Hasher un mot de passe"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    @staticmethod
    def verify_password(password, hashed_password):
        """Vérifier un mot de passe"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    @staticmethod
    def create_user(email, password, role, nom=None, prenom=None):
        """Créer un nouvel utilisateur"""
        db = DatabaseConnections.get_mongo_db()

        # Vérifier si l'utilisateur existe déjà
        if db.utilisateurs.find_one({"email": email}):
            return {"success": False, "message": "Cet email existe déjà"}

        # Hasher le mot de passe
        hashed_password = AuthService.hash_password(password)

        # Créer l'utilisateur
        user_data = {
            "email": email,
            "mot_de_passe": hashed_password,
            "role": role,
            "date_creation": datetime.now(),
            "actif": True
        }

        # Ajouter nom et prénom si fournis
        if nom:
            user_data["nom"] = nom
        if prenom:
            user_data["prenom"] = prenom

        try:
            result = db.utilisateurs.insert_one(user_data)
            return {
                "success": True,
                "message": "Utilisateur créé avec succès",
                "user_id": str(result.inserted_id)
            }
        except Exception as e:
            return {"success": False, "message": f"Erreur lors de la création: {str(e)}"}

    @staticmethod
    def authenticate_user(email, password):
        """Authentifier un utilisateur"""
        db = DatabaseConnections.get_mongo_db()

        # Trouver l'utilisateur
        user = db.utilisateurs.find_one({"email": email, "actif": True})

        if not user:
            return {"success": False, "message": "Email ou mot de passe incorrect"}

        # Vérifier le mot de passe
        if AuthService.verify_password(password, user["mot_de_passe"]):
            return {
                "success": True,
                "user": {
                    "id": str(user["_id"]),
                    "email": user["email"],
                    "role": user["role"],
                    "nom": user.get("nom", ""),
                    "prenom": user.get("prenom", "")
                }
            }
        else:
            return {"success": False, "message": "Email ou mot de passe incorrect"}

    @staticmethod
    def get_user_by_id(user_id):
        """Récupérer un utilisateur par son ID"""
        db = DatabaseConnections.get_mongo_db()
        try:
            user = db.utilisateurs.find_one({"_id": ObjectId(user_id), "actif": True})
            if user:
                return {
                    "id": str(user["_id"]),
                    "email": user["email"],
                    "role": user["role"],
                    "nom": user.get("nom", ""),
                    "prenom": user.get("prenom", "")
                }
        except:
            pass
        return None

# Décorateurs pour protéger les routes
def login_required(f):
    """Décorateur pour exiger une connexion"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_roles):
    """Décorateur pour exiger un rôle spécifique"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Vous devez être connecté', 'error')
                return redirect(url_for('login'))

            user = AuthService.get_user_by_id(session['user_id'])
            if not user or user['role'] not in required_roles:
                flash('Vous n\'avez pas les permissions nécessaires', 'error')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Décorateur pour exiger le rôle admin"""
    return role_required(['admin'])(f)

def medecin_required(f):
    """Décorateur pour exiger le rôle médecin ou admin"""
    return role_required(['admin', 'medecin'])(f)

def patient_required(f):
    """Décorateur pour exiger le rôle patient ou admin"""
    return role_required(['admin', 'patient'])(f)