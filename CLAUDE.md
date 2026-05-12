# SQL Agent — POC e-commerce

## Objectif
Agent qui répond à des questions business en langage naturel sur une base SQLite e-commerce.
Exemple de questions cibles :
- "Quel est le top 5 clients en CA sur Q3 ?"
- "Quel produit a le plus chuté en avril ?"

## Stack
- Python 3.12
- uv (gestionnaire de paquets)
- SQLite (base locale)
- API Anthropic (claude-sonnet)
- Faker (génération de données)

## Architecture
1. `seed_db.py` — génère la base SQLite avec Faker (1000 lignes)
2. `agent.py` — agent qui traduit NL → SQL → résultat → réponse

## Schéma de la base
- `clients` (id, nom, email, ville, date_inscription)
- `produits` (id, nom, categorie, prix_unitaire)
- `commandes` (id, client_id, date_commande, statut)
- `lignes_commande` (id, commande_id, produit_id, quantite, prix_unitaire)

## Règles
- Ne jamais exécuter de DELETE, DROP ou UPDATE
- Toujours valider le SQL avant exécution
- Répondre en français