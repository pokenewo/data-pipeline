# Data Pipeline — API to PostgreSQL

## Objectif

Ce projet implémente un pipeline de traitement de données inspiré d'une architecture ETL (Extract, Transform, Load).

Le pipeline extrait des données depuis une API REST publique, valide la qualité des données, puis les charge dans une base PostgreSQL dans une table de staging.

L’objectif est de reproduire les bonnes pratiques utilisées en Data Engineering :

séparation des étapes du pipeline
validation des données en amont
gestion des erreurs
idempotence
structuration claire du projet

Source de données utilisée :
https://jsonplaceholder.typicode.com/posts

## Architecture du pipeline

```text
API REST
   ↓
extract.py
   ↓
data_raw.json
   ↓
validate.py
   ↓
dlq.jsonl
   ↓
load.py
   ↓
PostgreSQL (staging_posts)
````


Et orchestration via :
````markdown
`main.py`
````

## Stack technique

- Python 3
- PostgreSQL
- psycopg2
- requests
- logging
- SQL

### Concepts Data Engineering appliqués :

- pipeline ETL
- staging layer
- validation de données
- DLQ (Dead Letter Queue)
- idempotence
- contraintes SQL
- gestion d’erreurs
- structuration modulaire


## Structure du projet
````text
pipeline_data/
├── app/
│   ├── extract.py
│   ├── validate.py
│   ├── load.py
│   ├── main.py
│
├── sql/
│   ├── schema.sql
│   ├── transformations.sql
│
├── data_raw.json
├── dlq.jsonl
├── README.md
├── .gitignore
````

## Fonctionnement détaillé

extract.py
- appelle l'API REST
- sauvegarde les données brutes dans data_raw.json

validate.py
- vérifie la structure des données
- filtre les enregistrements invalides
- stocke les erreurs dans dlq.jsonl

load.py
- insère les données validées dans PostgreSQL
- évite les doublons grâce à ON CONFLICT DO NOTHING

## Installation

Cloner le projet :
````bash
git clone [data_pipeline](https://github.com/pokenewo/data-pipeline.git)
cd pipeline_data
````

Installer les dépendances :

```bash
pip install requests psycopg2-binary
```

Créer la base PostgreSQL :

```bash
createdb pipeline_db
```

Créer la table staging :

```bash
psql -d pipeline_db -f sql/schema.sql
```

## Utilisation

Lancer le pipeline :

```bash
python3 app/main.py
```

Le pipeline exécute les étapes suivantes :

1. extraction depuis l'API
2. validation des données
3. chargement dans PostgreSQL

## Exemple de logs

Premier lancement :

```text
Records inserted: 100
Records skipped: 0
Pipeline completed successfully.
```

Relancement du pipeline :

```text
Records inserted: 0
Records skipped: 100
Pipeline completed successfully.
```

Cela montre que le pipeline est idempotent.

## Qualité des données

La validation garantit :

- présence des champs obligatoires
- types corrects
- absence de valeurs nulles
- titre non vide

Les données invalides sont stockées dans :
`dlq.jsonl`

Chaque ligne correspond à un enregistrement rejeté.

## Idempotence du pipeline

Le chargement utilise :

```sql
ON CONFLICT (post_id) DO NOTHING
```

Cela permet :

- de relancer le pipeline sans créer de doublons
- de rejouer le traitement en cas d'erreur
- de rendre le pipeline robuste

## Modèle de données (staging)

Table :

`staging_posts`

Colonnes :

- user_id
- post_id (clé primaire)
- title
- body

Contraintes :

- clé primaire sur post_id
- vérification user_id > 0
- title non vide

## Améliorations futures

- ajout d’une couche de transformation SQL
- ajout de tests unitaires (pytest)
- dockerisation du pipeline
- orchestration avec Airflow
- gestion des variables d’environnement
- logs structurés
- ajout d’une table clean
- monitoring du pipeline

