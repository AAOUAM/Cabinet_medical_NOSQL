from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from .Config import  Config, DatabaseConnections
from .services.auth_service import (AuthService, login_required, admin_required, medecin_required, patient_required)

import atexit

app = Flask(__name__)
app.config.from_object(Config)

# Fermer les connexions à la fin de l'application
@atexit.register
def cleanup():
    DatabaseConnections.close_connections()

# ==================== ROUTES D'AUTHENTIFICATION ====================

@app.route('/')
def index():
    """Page d'accueil - Redirection vers login si non connecté"""
    if 'user_id' in session:
        user_role = session.get('user_role')
        if user_role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user_role == 'medecin':
            return redirect(url_for('medecin_dashboard'))
        elif user_role == 'patient':
            return redirect(url_for('patient_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    # Si déjà connecté, rediriger vers le dashboard approprié
    if 'user_id' in session:
        user_role = session.get('user_role')
        if user_role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user_role == 'medecin':
            return redirect(url_for('medecin_dashboard'))
        elif user_role == 'patient':
            return redirect(url_for('patient_dashboard'))


    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        # Validation des champs
        if not email or not password:
            flash('Veuillez remplir tous les champs', 'error')
            return render_template('auth/login.html')

        # Tentative d'authentification
        result = AuthService.authenticate_user(email, password)

        if result['success']:
            user = result['user']

            # Créer la session utilisateur
            session.permanent = True  # Session persistante
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            session['user_nom'] = user.get('nom', '')
            session['user_prenom'] = user.get('prenom', '')

            # Message de bienvenue personnalisé
            nom_complet = f"{user.get('prenom', '')} {user.get('nom', '')}".strip()
            if nom_complet:
                flash(f'Bienvenue {nom_complet}!', 'success')
            else:
                flash(f'Bienvenue {user["email"]}!', 'success')

            # Redirection selon le rôle
            user_role = user['role']
            if user_role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user_role == 'medecin':
                return redirect(url_for('medecin_dashboard'))
            elif user_role == 'patient':
                return redirect(url_for('patient_dashboard'))
            else:
                # Rôle par défaut ou inconnu
                return redirect(url_for('dashboard'))
        else:
            flash(result['message'], 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Déconnexion utilisateur"""
    # Sauvegarder le nom pour le message d'au revoir
    user_name = session.get('user_prenom', '') or session.get('user_email', 'Utilisateur')

    # Nettoyer la session
    session.clear()

    flash(f'Au revoir {user_name}! Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))

