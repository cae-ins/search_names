# 🔍 Search Names API - Côte d'Ivoire Census 2021

[![Django](https://img.shields.io/badge/Django-4.2-brightgreen)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-24.0-blue)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)
[![ElasticSearch](https://img.shields.io/badge/ElasticSearch-8.8-orange)](https://www.elastic.co/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

API de recherche de noms basée sur les données du recensement ivoirien 2021, permettant d'obtenir des statistiques détaillées sur l'utilisation des noms et prénoms.

## 🌟 Fonctionnalités

- 🔎 Recherche exacte et floue de noms
- 📊 Statistiques détaillées par genre :
  - Nombre d'occurrences comme prénom/nom de famille
  - Utilisation comme prénom unique
  - Répartition homme/femme
- 🤖 Suggestions automatiques de noms similaires
- 🚀 Architecture scalable avec Docker
- 📈 Dashboard d'administration Django

## 🛠 Stack Technique

| Composant               | Technologie                          |
|-------------------------|--------------------------------------|
| **Backend**             | Django 4.2 + Django REST Framework   |
| **Moteur de recherche** | ElasticSearch 8.8                    |
| **Infrastructure**      | Docker + Nginx                       |
| **Monitoring**          | Prometheus + Grafana (optionnel)     |

## 🚀 Démarrage Rapide

### Prérequis
- Docker 24.0+
- Docker Compose 2.20+

### Installation
```bash
git clone git@github.com:cae-ins/search_names.git
cd search_names

# Créer le fichier d'environnement
cp .env.example .env

# Démarrer les services
docker-compose up -d --build

# Appliquer les migrations
docker-compose exec django python manage.py migrate

# Importer les données initiales
docker-compose exec django python manage.py import_data
```
# Documentation API
```bash
GET /api/search/?q={nom}&fuzzy={true|false}
```
Paramètres :

q : Nom à rechercher (obligatoire)

fuzzy : Active la recherche approximative 
```bash
Exemple de réponse :
{{
  "nom": "Kouadio",
  "statistiques": {
    "partie_prenom": 1500,
    "nom_famille": 300,
    "prenom_unique": 200,
    "nombre_homme_prenom": 800,
    "...": "..."
  }
}
```
 # Schémas des Données
 ```bash
{{
  "Nom": {
    "type": "string",
    "example": "Kouadio"
  },
  "Statistiques": {
    "partie_prenom": "integer",
    "nom_famille": "integer",
    "prenom_unique": "integer",
    "nombre_homme_prenom": "integer",
    "nombre_homme_nom_famille": "integer",
    "nombre_femme_prenom": "integer",
    "nombre_femme_nom_famille": "integer"
  }
```

# 📬 Contact
Pour toute question ou support :

Responsable Technique : j.migone@stat.plan.gouv.ci

Équipe : DataLab ANStat

Site Web : https://www.anstat.ci
