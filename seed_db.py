import random
import sqlite3
from datetime import datetime, timedelta

from faker import Faker

DB_PATH = "ecommerce.db"
SEED = 42

fake = Faker("fr_FR")
Faker.seed(SEED)
random.seed(SEED)

VILLES = [
    "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg",
    "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre",
    "Saint-Étienne", "Toulon", "Grenoble", "Dijon", "Angers", "Nîmes", "Villeurbanne",
]

CATEGORIES = ["Électronique", "Vêtements", "Maison", "Sport", "Beauté"]

STATUTS = ["livré", "en cours", "annulé"]
STATUT_WEIGHTS = [0.70, 0.20, 0.10]


def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def weighted_date(start: datetime, end: datetime) -> datetime:
    """Génère une date avec pic en nov-déc (saisonnalité Black Friday / Noël)."""
    month = random.choices(
        range(1, 13),
        weights=[5, 5, 6, 6, 7, 7, 7, 7, 7, 8, 14, 21],
    )[0]
    year = random.randint(start.year, end.year)
    year = max(start.year, min(end.year, year))
    max_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    day = random.randint(1, max_day)
    candidate = datetime(year, month, day)
    if candidate < start:
        candidate = start
    if candidate > end:
        candidate = end
    return candidate


def seed(db_path: str = DB_PATH) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS lignes_commande;
        DROP TABLE IF EXISTS commandes;
        DROP TABLE IF EXISTS produits;
        DROP TABLE IF EXISTS clients;

        CREATE TABLE clients (
            id               INTEGER PRIMARY KEY,
            nom              TEXT NOT NULL,
            email            TEXT NOT NULL UNIQUE,
            ville            TEXT NOT NULL,
            date_inscription TEXT NOT NULL
        );

        CREATE TABLE produits (
            id             INTEGER PRIMARY KEY,
            nom            TEXT NOT NULL,
            categorie      TEXT NOT NULL,
            prix_unitaire  REAL NOT NULL
        );

        CREATE TABLE commandes (
            id             INTEGER PRIMARY KEY,
            client_id      INTEGER NOT NULL REFERENCES clients(id),
            date_commande  TEXT NOT NULL,
            statut         TEXT NOT NULL
        );

        CREATE TABLE lignes_commande (
            id           INTEGER PRIMARY KEY,
            commande_id  INTEGER NOT NULL REFERENCES commandes(id),
            produit_id   INTEGER NOT NULL REFERENCES produits(id),
            quantite     INTEGER NOT NULL,
            prix_unitaire REAL NOT NULL
        );
    """)

    # --- clients (200) ---
    clients = []
    emails_seen: set[str] = set()
    # 20 gros clients auront 3x plus de commandes
    gros_clients_ids = set(range(1, 21))

    for i in range(1, 201):
        nom = fake.name()
        email = fake.unique.email()
        emails_seen.add(email)
        ville = random.choice(VILLES)
        date_inscription = random_date(
            datetime(2022, 1, 1), datetime(2025, 12, 31)
        ).strftime("%Y-%m-%d")
        clients.append((i, nom, email, ville, date_inscription))

    cur.executemany(
        "INSERT INTO clients VALUES (?, ?, ?, ?, ?)", clients
    )

    # --- produits (50) ---
    produits = []
    for i in range(1, 51):
        categorie = random.choice(CATEGORIES)
        nom = f"{fake.word().capitalize()} {categorie[:3]}-{i}"
        prix = round(random.uniform(5.0, 500.0), 2)
        produits.append((i, nom, categorie, prix))

    cur.executemany(
        "INSERT INTO produits VALUES (?, ?, ?, ?)", produits
    )

    # Prix de base par produit (dict id → prix) pour snapshot lignes_commande
    prix_base = {p[0]: p[3] for p in produits}

    # --- commandes + lignes_commande ---
    start_cmd = datetime(2023, 1, 1)
    end_cmd = datetime(2025, 12, 31)

    commande_id = 0
    ligne_id = 0
    commandes_rows = []
    lignes_rows = []

    for client_id in range(1, 201):
        # Gros clients : 5–15 commandes ; autres : 1–7
        if client_id in gros_clients_ids:
            nb_commandes = random.randint(5, 15)
        else:
            nb_commandes = random.randint(1, 7)

        for _ in range(nb_commandes):
            commande_id += 1
            date_cmd = weighted_date(start_cmd, end_cmd).strftime("%Y-%m-%d")
            statut = random.choices(STATUTS, weights=STATUT_WEIGHTS)[0]
            commandes_rows.append((commande_id, client_id, date_cmd, statut))

            nb_lignes = random.randint(1, 5)
            produits_choisis = random.sample(range(1, 51), k=nb_lignes)
            for prod_id in produits_choisis:
                ligne_id += 1
                quantite = random.randint(1, 5)
                # Snapshot prix : légère variation ±10 %
                prix_snap = round(prix_base[prod_id] * random.uniform(0.90, 1.10), 2)
                lignes_rows.append((ligne_id, commande_id, prod_id, quantite, prix_snap))

    cur.executemany(
        "INSERT INTO commandes VALUES (?, ?, ?, ?)", commandes_rows
    )
    cur.executemany(
        "INSERT INTO lignes_commande VALUES (?, ?, ?, ?, ?)", lignes_rows
    )

    conn.commit()

    # --- résumé ---
    print("Base générée :", db_path)
    for table in ("clients", "produits", "commandes", "lignes_commande"):
        (count,) = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        print(f"  {table:<20} {count:>6} lignes")

    conn.close()


if __name__ == "__main__":
    seed()
