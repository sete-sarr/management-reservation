# Management Reservation

## FR — Vue d’ensemble

**Management Reservation** est une application web Django dédiée à la gestion des réservations de voyages. Elle permet aux utilisateurs de parcourir des destinations, de consulter les détails, de réserver des voyages, de suivre leurs réservations, de laisser des avis et de gérer leur profil.

Le projet est structuré autour de plusieurs applications Django spécialisées :
- `destinations` pour les offres et la recherche
- `bookings` pour la gestion des réservations
- `payments` pour le suivi des paiements
- `reviews` pour les avis utilisateurs
- `users` pour l’authentification et les profils

## EN — Overview

**Management Reservation** is a Django web application designed for managing travel reservations. It allows users to browse destinations, view details, book trips, track reservations, leave reviews, and manage their profile.

The project is organized into several specialized Django apps:
- `destinations` for offers and search
- `bookings` for reservation management
- `payments` for payment tracking
- `reviews` for user reviews
- `users` for authentication and profiles

---

## FR — Fonctionnalités principales

### Pour les utilisateurs
- Recherche et filtrage des destinations par pays, prix, note et disponibilité
- Consultation d’une page détaillée par destination
- Réservation avec dates de voyage, nombre de voyageurs et demandes spéciales
- Suivi des réservations (pending, confirmed, cancelled, completed)
- Gestion du profil utilisateur
- Ajout et modification d’avis sur les destinations
- Interface responsive et moderne

### Pour les administrateurs
- Tableau de bord avec statistiques globales
- Gestion des destinations
- Gestion des réservations et de leur état
- Suivi des paiements
- Modération des avis
- Accès au panneau d’administration Django

## EN — Key Features

### For users
- Search and filter destinations by country, price, rating, and availability
- View detailed destination pages
- Book trips with travel dates, traveler count, and special requests
- Track bookings (pending, confirmed, cancelled, completed)
- Manage user profile information
- Add and update reviews for destinations
- Responsive and modern interface

### For admins
- Dashboard with global statistics
- Destination management
- Booking management and status updates
- Payment tracking
- Review moderation
- Access to Django admin panel

---

## FR — Stack technique

- Python 3.10+
- Django
- SQLite (développement) / PostgreSQL possible en production
- Bootstrap 5 pour l’interface
- Pillow pour la gestion des images
- Django REST Framework (présent dans les dépendances)
- Redis / Django Debug Toolbar (configurations et outils liés au projet)

## EN — Tech Stack

- Python 3.10+
- Django
- SQLite (development) / PostgreSQL possible in production
- Bootstrap 5 for the UI
- Pillow for image handling
- Django REST Framework (included in dependencies)
- Redis / Django Debug Toolbar (related tooling)

---

## FR — Structure du projet

```text
management_reservation/
├── bookings/               # Gestion des réservations
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── destinations/           # Destinations et pages principales
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templatetags/
├── payments/               # Paiements et statuts
│   ├── models.py
│   ├── views.py
│   └── admin.py
├── reviews/                # Avis clients
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── users/                  # Authentification et profils
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── management_reservation/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/              # Templates HTML
├── static/                 # Fichiers statiques CSS/JS/images
├── media/                  # Fichiers uploadés
├── requirements.txt
├── manage.py
├── create_superuser.py
├── docker-compose.yml
└── README.md
```

## EN — Project Structure

```text
management_reservation/
├── bookings/               # Booking management
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── destinations/           # Destinations and main pages
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templatetags/
├── payments/               # Payments and statuses
│   ├── models.py
│   ├── views.py
│   └── admin.py
├── reviews/                # Customer reviews
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── users/                  # Authentication and profiles
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── management_reservation/
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── templates/              # HTML templates
├── static/                 # Static files (CSS/JS/images)
├── media/                  # Uploaded files
├── requirements.txt
├── manage.py
├── create_superuser.py
├── docker-compose.yml
└── README.md
```

---

## FR — Prérequis

- Python 3.10 ou supérieur
- pip
- virtualenv (recommandé)
- Git
- Un navigateur web moderne

## EN — Prerequisites

- Python 3.10 or higher
- pip
- virtualenv (recommended)
- Git
- A modern web browser

---

## FR — Installation et lancement

### 1) Cloner le projet

```bash
git clone <url-du-repo>
cd management_reservation
```

### 2) Créer un environnement virtuel

```bash
python -m venv venv
```

Sur Windows :

```bash
venv\Scripts\activate
```

Sur Linux/macOS :

```bash
source venv/bin/activate
```

### 3) Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4) Configurer les paramètres Django

Le projet contient plusieurs fichiers de configuration dans [management_reservation/settings](management_reservation/settings).

Pour le développement local, vous pouvez exécuter :

```bash
python manage.py runserver --settings=management_reservation.settings.local
```

### 5) Appliquer les migrations

```bash
python manage.py migrate
```

### 6) Créer un superutilisateur

```bash
python manage.py createsuperuser
```

Ou via le script fourni :

```bash
python create_superuser.py
```

### 7) Lancer l’application

```bash
python manage.py runserver
```

Accès local :
- Frontend : http://localhost:8000/
- Administration : http://localhost:8000/admin/

## EN — Installation and Running

### 1) Clone the project

```bash
git clone <repo-url>
cd management_reservation
```

### 2) Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure Django settings

The project contains several settings files in [management_reservation/settings](management_reservation/settings).

For local development, you can run:

```bash
python manage.py runserver --settings=management_reservation.settings.local
```

### 5) Apply migrations

```bash
python manage.py migrate
```

### 6) Create a superuser

```bash
python manage.py createsuperuser
```

Or with the provided script:

```bash
python create_superuser.py
```

### 7) Start the app

```bash
python manage.py runserver
```

Local URLs:
- Frontend: http://localhost:8000/
- Admin: http://localhost:8000/admin/

---

## FR — Modèles principaux

### Destination
- nom, pays, description
- prix par personne
- nombre de places disponibles
- image, durée du séjour, note, nombre d’avis
- statut mis en avant / actif

### UserProfile
- téléphone, adresse, ville, pays, code postal
- photo de profil, biographie
- statut de vérification
- statistiques de réservation

### Booking
- utilisateur, destination, dates de voyage
- nombre de voyageurs
- prix total
- statut et code de confirmation
- demandes spéciales

### Payment
- réservation liée
- montant, méthode de paiement, statut
- identifiant de transaction, date de paiement
- remboursement si applicable

### Review
- utilisateur, destination, notation sur 5
- titre, commentaires
- indication si la réservation est vérifiée
- compteur utile / inutile

## EN — Main Models

### Destination
- name, country, description
- price per person
- available slots
- image, trip duration, rating, review count
- featured / active status

### UserProfile
- phone, address, city, country, postal code
- profile picture, bio
- verification status
- booking statistics

### Booking
- user, destination, travel dates
- number of travelers
- total price
- status and confirmation code
- special requests

### Payment
- linked booking
- amount, payment method, status
- transaction ID, payment date
- refund details if applicable

### Review
- user, destination, rating out of 5
- title, comments
- verified booking indicator
- helpful / unhelpful counters

---

## FR — Routes principales

### Pages publiques
- `/` : page d’accueil
- `/browse/` : liste des destinations
- `/<nom-destination>/` : détail d’une destination
- `/auth/register/` : inscription
- `/auth/login/` : connexion

### Pages utilisateur connecté
- `/bookings/` : liste des réservations
- `/bookings/<id>/` : détail d’une réservation
- `/bookings/<destination>/create/` : créer une réservation
- `/bookings/<id>/cancel/` : annuler une réservation
- `/auth/profile/` : profil
- `/auth/profile/update/` : modifier le profil
- `/reviews/<destination>/create/` : ajouter un avis

### Administration
- `/admin/` : panneau d’administration
- `/bookings/dashboard/` : tableau de bord administrateur

## EN — Main Routes

### Public pages
- `/` : home page
- `/browse/` : destination list
- `/<destination-name>/` : destination details
- `/auth/register/` : registration
- `/auth/login/` : login

### Authenticated pages
- `/bookings/` : booking list
- `/bookings/<id>/` : booking details
- `/bookings/<destination>/create/` : create booking
- `/bookings/<id>/cancel/` : cancel booking
- `/auth/profile/` : profile
- `/auth/profile/update/` : update profile
- `/reviews/<destination>/create/` : add review

### Administration
- `/admin/` : admin panel
- `/bookings/dashboard/` : admin dashboard

---

## FR — Déploiement

Pour un déploiement en production :
1. Mettre `DEBUG` à `False`
2. Définir correctement `ALLOWED_HOSTS`
3. Utiliser une base de données robuste (PostgreSQL recommandé)
4. Configurer les variables d’environnement sensibles
5. Servir les fichiers statiques correctement
6. Utiliser un serveur WSGI tel que Gunicorn
7. Configurer HTTPS et les en-têtes de sécurité

## EN — Deployment

For production deployment:
1. Set `DEBUG` to `False`
2. Configure `ALLOWED_HOSTS` correctly
3. Use a robust database (PostgreSQL recommended)
4. Configure sensitive environment variables
5. Serve static files correctly
6. Use a WSGI server such as Gunicorn
7. Configure HTTPS and security headers

---

## FR — Dépannage rapide

### Le serveur ne démarre pas
```bash
python manage.py check
```

### Erreur de base de données
```bash
python manage.py migrate
```

### Port déjà utilisé
```bash
python manage.py runserver 8001
```

### Fichiers statiques manquants
```bash
python manage.py collectstatic
```

## EN — Quick Troubleshooting

### Server does not start
```bash
python manage.py check
```

### Database error
```bash
python manage.py migrate
```

### Port already in use
```bash
python manage.py runserver 8001
```

### Missing static files
```bash
python manage.py collectstatic
```

---

## FR — Notes importantes

- Le fichier [management_reservation/settings](management_reservation/settings) contient plusieurs environnements (base, local, prod).
- Le script [create_superuser.py](create_superuser.py) permet de créer rapidement un administrateur.
- Les médias uploadés sont stockés dans le dossier `media/` pendant le développement.
- Le projet utilise les templates Django avec des vues basées sur les classes.

## EN — Important Notes

- The [management_reservation/settings](management_reservation/settings) folder contains several environments (base, local, prod).
- The [create_superuser.py](create_superuser.py) script allows you to quickly create an administrator.
- Uploaded media files are stored in the `media/` folder during development.
- The project uses Django templates together with class-based views.

---

## FR — Contribution

Les contributions sont les bienvenues. Pour proposer une amélioration :
1. Créer une branche
2. Appliquer les modifications
3. Tester le comportement attendu
4. Ouvrir une pull request

## EN — Contribution

Contributions are welcome. To propose an improvement:
1. Create a branch
2. Apply your changes
3. Test the expected behavior
4. Open a pull request

---

## FR — Licence

Ce projet est fourni à titre éducatif et peut être adapté selon vos besoins.

## EN — License

This project is provided for educational purposes and can be adapted to your needs.
