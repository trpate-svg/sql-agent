import re
import sqlite3
from datetime import date

import anthropic
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "ecommerce.db"
MODEL = "claude-sonnet-4-6"

SCHEMA = """
Tables disponibles :

clients (id, nom, email, ville, date_inscription)
produits (id, nom, categorie, prix_unitaire)
commandes (id, client_id, date_commande, statut)
  - statut : 'livré', 'en cours', 'annulé'
lignes_commande (id, commande_id, produit_id, quantite, prix_unitaire)
  - prix_unitaire : snapshot du prix au moment de la commande

Relations :
  commandes.client_id → clients.id
  lignes_commande.commande_id → commandes.id
  lignes_commande.produit_id → produits.id

Calcul du CA : SUM(quantite * prix_unitaire) sur lignes_commande
"""

SQL_BLACKLIST = re.compile(
    r"\b(DELETE|DROP|UPDATE|INSERT|ALTER|TRUNCATE|CREATE|REPLACE|MERGE)\b",
    re.IGNORECASE,
)

client = anthropic.Anthropic()


def _system_sql() -> str:
    return f"""Tu es un expert SQL SQLite. Tu traduis des questions business en requêtes SQL.

{SCHEMA}

Date du jour : {date.today().isoformat()}

Règles strictes :
- Réponds UNIQUEMENT avec la requête SQL, sans explication ni markdown.
- La requête doit commencer par SELECT.
- N'utilise jamais DELETE, DROP, UPDATE, INSERT, ALTER.
- Utilise des alias clairs (ex: SUM(...) AS ca_total).
- Limite les résultats à 20 lignes sauf si la question demande explicitement plus.
"""


def generate_sql(question: str) -> str:
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=_system_sql(),
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text.strip()


def validate_sql(sql: str) -> tuple[bool, str]:
    stripped = sql.strip().lstrip(";").strip()
    if not stripped.upper().startswith("SELECT"):
        return False, "La requête doit commencer par SELECT."
    match = SQL_BLACKLIST.search(stripped)
    if match:
        return False, f"Mot-clé interdit détecté : {match.group().upper()}"
    return True, ""


def execute_sql(sql: str) -> list[dict]:
    uri = f"file:{DB_PATH}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(sql)
        rows = [dict(row) for row in cursor.fetchall()]
        return rows
    finally:
        conn.close()


def format_response(question: str, sql: str, rows: list[dict]) -> str:
    if not rows:
        result_text = "Aucun résultat."
    else:
        headers = list(rows[0].keys())
        lines = [" | ".join(headers)]
        lines.append("-" * len(lines[0]))
        for row in rows:
            lines.append(" | ".join(str(v) for v in row.values()))
        result_text = "\n".join(lines)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=(
            "Tu es un analyste business francophone. "
            "Tu reçois une question, la requête SQL exécutée, et les résultats bruts. "
            "Formule une réponse claire en français, avec contexte business si pertinent. "
            "Si les résultats sont tabulaires, présente-les en markdown table."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Question : {question}\n\n"
                f"SQL exécuté :\n```sql\n{sql}\n```\n\n"
                f"Résultats :\n{result_text}"
            ),
        }],
    )
    return response.content[0].text.strip()


def answer(question: str) -> str:
    sql = generate_sql(question)

    valid, error = validate_sql(sql)
    if not valid:
        # Un seul retry avec le message d'erreur
        sql = generate_sql(
            f"{question}\n\n[Correction requise : {error} — génère une requête SELECT valide.]"
        )
        valid, error = validate_sql(sql)
        if not valid:
            return f"Impossible de générer une requête valide : {error}"

    try:
        rows = execute_sql(sql)
    except sqlite3.OperationalError as e:
        return f"Erreur SQL : {e}\n\nRequête tentée :\n```sql\n{sql}\n```"
    except sqlite3.DatabaseError as e:
        return f"Erreur base de données : {e}"

    if not rows:
        return "Aucun résultat trouvé pour cette requête."

    return format_response(question, sql, rows)


def main() -> None:
    print("Agent SQL e-commerce — tapez 'exit' pour quitter.\n")
    while True:
        try:
            question = input("Question : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            break

        if not question:
            continue
        if question.lower() in {"exit", "quit", "q"}:
            print("Au revoir !")
            break

        print()
        print(answer(question))
        print()


if __name__ == "__main__":
    main()
