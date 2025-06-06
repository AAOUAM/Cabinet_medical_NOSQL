#!/usr/bin/env python3
"""
Script pour créer une structure complète de données de test
avec liaison entre utilisateurs et données métier
"""

import bcrypt
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB_NAME = "cabinet_db"

def hash_password(password):
    """Hasher un mot de passe"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def create_complete_test_data():
    """Créer des données de test complètes avec liaisons"""

    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]

    print("🗑️  Nettoyage des collections existantes...")
    # Optionnel : vider les collections
    # db.utilisateurs.delete_many({})
    # db.patients.delete_many({})
    # db.medecins.delete_many({})
    # db.consultations.delete_many({})

    # ==================== CRÉATION DES UTILISATEURS ====================
    print("\n👥 Création des utilisateurs...")

    # 1. Administrateur
    admin_id = db.utilisateurs.insert_one({
        "email": "admin@cabinet.com",
        "mot_de_passe": hash_password("admin123"),
        "role": "admin",
        "date_creation": datetime.now(),
        "actif": True
    }).inserted_id
    print(f"✅ Admin créé: {admin_id}")

    # 2. Médecins (utilisateurs)
    medecin1_user_id = db.utilisateurs.insert_one({
        "email": "dr.amine@gmail.com",
        "mot_de_passe": hash_password("medecin123"),
        "role": "medecin",
        "date_creation": datetime.now(),
        "actif": True
    }).inserted_id

    medecin2_user_id = db.utilisateurs.insert_one({
        "email": "dr.sophie@gmail.com",
        "mot_de_passe": hash_password("medecin123"),
        "role": "medecin",
        "date_creation": datetime.now(),
        "actif": True
    }).inserted_id

    # 3. Patients (utilisateurs)
    patient1_user_id = db.utilisateurs.insert_one({
        "email": "ahmed.taha@gmail.com",
        "mot_de_passe": hash_password("patient123"),
        "role": "patient",
        "date_creation": datetime.now(),
        "actif": True
    }).inserted_id

    patient2_user_id = db.utilisateurs.insert_one({
        "email": "marie.bernard@gmail.com",
        "mot_de_passe": hash_password("patient123"),
        "role": "patient",
        "date_creation": datetime.now(),
        "actif": True
    }).inserted_id

    # ==================== CRÉATION DES MÉDECINS (DONNÉES MÉTIER) ====================
    print("\n🩺 Création des médecins (données métier)...")

    medecin1_id = db.medecins.insert_one({
        "user_id": str(medecin1_user_id),  # 🔗 LIAISON avec utilisateur
        "nom": "Dr. Amine",
        "specialite": "Cardiologie",
        "adresse": "Polyclinique Al Andalous, Agadir",
        "num_tel": "0600000000",
        "email": "dr.amine@gmail.com",
        "disponibilite": ["Lundi", "Mercredi", "Vendredi"],
        "experiences": "10 ans en cardiologie"
    }).inserted_id

    medecin2_id = db.medecins.insert_one({
        "user_id": str(medecin2_user_id),  # 🔗 LIAISON avec utilisateur
        "nom": "Dr. Sophie",
        "specialite": "Pédiatrie",
        "adresse": "Clinique des Enfants, Agadir",
        "num_tel": "0600000001",
        "email": "dr.sophie@gmail.com",
        "disponibilite": ["Mardi", "Jeudi", "Samedi"],
        "experiences": "8 ans en pédiatrie"
    }).inserted_id

    print(f"✅ Médecins créés: {medecin1_id}, {medecin2_id}")

    # ==================== CRÉATION DES PATIENTS (DONNÉES MÉTIER) ====================
    print("\n🏥 Création des patients (données métier)...")

    patient1_id = db.patients.insert_one({
        "user_id": str(patient1_user_id),  # 🔗 LIAISON avec utilisateur
        "nom": "Ahmed",
        "prenom": "Taha",
        "age": 35,
        "sexe": "H",
        "date_naissance": "1990-04-12",
        "num_tel": "0600000000",
        "email": "ahmed.taha@gmail.com",
        "adresse": "Rue des Roses, Agadir"
    }).inserted_id

    patient2_id = db.patients.insert_one({
        "user_id": str(patient2_user_id),  # 🔗 LIAISON avec utilisateur
        "nom": "Bernard",
        "prenom": "Marie",
        "age": 28,
        "sexe": "F",
        "date_naissance": "1996-08-15",
        "num_tel": "0600000002",
        "email": "marie.bernard@gmail.com",
        "adresse": "Avenue Mohammed V, Agadir"
    }).inserted_id

    print(f"✅ Patients créés: {patient1_id}, {patient2_id}")

    # ==================== CRÉATION DES CONSULTATIONS ====================
    print("\n📋 Création des consultations...")

    consultation1_id = db.consultations.insert_one({
        "id_patient": str(patient1_id),
        "id_medecin": str(medecin1_id),
        "date": "2025-06-02",
        "diagnostic": "Hypertension",
        "traitement": "Repos + médicament",
        "ordonnance": "Paracétamol 500mg - 2x/jour pendant 5 jours",
        "notes": "Patient stressé, prévoir contrôle dans 1 mois"
    }).inserted_id

    consultation2_id = db.consultations.insert_one({
        "id_patient": str(patient2_id),
        "id_medecin": str(medecin2_id),
        "date": "2025-06-03",
        "diagnostic": "Grippe saisonnière",
        "traitement": "Repos et hydratation",
        "ordonnance": "Doliprane 1000mg - 3x/jour pendant 3 jours",
        "notes": "Symptômes légers, guérison rapide attendue"
    }).inserted_id

    print(f"✅ Consultations créées: {consultation1_id}, {consultation2_id}")

    client.close()
    print("\n🎉 Base de données créée avec succès!")

def show_complete_credentials():
    """Afficher tous les identifiants de test"""
    print("\n" + "="*70)
    print("🔑 IDENTIFIANTS DE TEST POUR VOTRE APPLICATION")
    print("="*70)

    print("\n👑 ADMINISTRATEUR:")
    print("   📧 Email: admin@cabinet.com")
    print("   🔑 Mot de passe: admin123")
    print("   ℹ️  Accès: Toutes les fonctionnalités")

    print("\n🩺 MÉDECINS:")
    print("   📧 Email: dr.amine@gmail.com")
    print("   🔑 Mot de passe: medecin123")
    print("   ℹ️  Spécialité: Cardiologie")

    print("   📧 Email: dr.sophie@gmail.com")
    print("   🔑 Mot de passe: medecin123")
    print("   ℹ️  Spécialité: Pédiatrie")

    print("\n🏥 PATIENTS:")
    print("   📧 Email: ahmed.taha@gmail.com")
    print("   🔑 Mot de passe: patient123")
    print("   ℹ️  Nom: Ahmed Taha")

    print("   📧 Email: marie.bernard@gmail.com")
    print("   🔑 Mot de passe: patient123")
    print("   ℹ️  Nom: Marie Bernard")

    print("\n" + "="*70)
    print("💡 STRUCTURE DE LIAISON:")
    print("   • Collection 'utilisateurs' → Authentification + Rôles")
    print("   • Collections 'patients'/'medecins' → Données métier")
    print("   • Champ 'user_id' → Liaison entre les deux")
    print("="*70)

if __name__ == "__main__":
    try:
        create_complete_test_data()
        show_complete_credentials()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("Assurez-vous que MongoDB est démarré et accessible.")