import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import date
from typing import Optional

import anthropic
from dotenv import load_dotenv

load_dotenv()

from agent import answer_with_sql

MODEL = "claude-sonnet-4-6"
SLEEP_BETWEEN_S = 1.5

JUDGE_SYSTEM = """\
Tu es un évaluateur de systèmes d'analyse de données (BI/SQL).
Tu reçois : une question business, des critères attendus pour une bonne réponse, \
et la réponse produite par un agent SQL.

Note la réponse de 0 à 2 :
- 2 : réponse correcte et complète — contient toutes les informations demandées, \
cohérente avec la question
- 1 : réponse partiellement correcte — bonne direction mais info manquante, \
imprécise ou ambiguïté non gérée
- 0 : réponse incorrecte, erreur SQL, hors sujet, données absentes sans justification, \
ou refus injustifié

Règles :
- Les critères attendus sont des guides, pas des valeurs exactes à vérifier.
- Pour les questions ambiguës, une bonne réponse doit expliciter l'interprétation choisie.
- Une erreur technique (SQL invalide, exception Python) vaut toujours 0.

Réponds UNIQUEMENT avec un objet JSON valide sur une seule ligne :
{"score": <0, 1 ou 2>, "verdict": "<explication courte en français, max 100 caractères>"}\
"""

QUESTIONS = [
    # ── Top/flop simples (8) ──────────────────────────────────────────────────
    {
        "category": "Top/flop simples",
        "question": "Quel est le top 5 clients en chiffre d'affaires total ?",
        "expected": (
            "doit lister 5 noms de clients avec leur CA en euros, "
            "triés du plus grand au plus petit"
        ),
    },
    {
        "category": "Top/flop simples",
        "question": "Quel est le produit le plus vendu en quantité totale ?",
        "expected": (
            "doit mentionner le nom d'un produit et sa quantité totale vendue"
        ),
    },
    {
        "category": "Top/flop simples",
        "question": "Quelle catégorie de produits génère le plus de chiffre d'affaires ?",
        "expected": (
            "doit nommer une des 5 catégories (Électronique, Vêtements, Maison, Sport, Beauté) "
            "avec son CA total en euros"
        ),
    },
    {
        "category": "Top/flop simples",
        "question": "Quels sont les 3 produits les moins vendus en quantité ?",
        "expected": (
            "doit lister 3 produits avec leurs quantités vendues, "
            "triés du moins vendu au plus vendu"
        ),
    },
    {
        "category": "Top/flop simples",
        "question": "Quel client a passé le plus grand nombre de commandes ?",
        "expected": (
            "doit mentionner un nom de client et son nombre total de commandes"
        ),
    },
    {
        "category": "Top/flop simples",
        "question": "Quelle ville génère le plus de chiffre d'affaires total ?",
        "expected": (
            "doit nommer une ville française avec son CA total en euros"
        ),
    },
    {
        "category": "Top/flop simples",
        "question": "Quel est le produit le plus cher du catalogue ?",
        "expected": (
            "doit mentionner le nom d'un produit et son prix unitaire en euros"
        ),
    },
    {
        "category": "Top/flop simples",
        "question": "Quels sont les 5 produits avec le CA total le plus élevé ?",
        "expected": (
            "doit lister 5 produits avec leur CA total en euros, "
            "triés du plus grand au plus petit"
        ),
    },

    # ── Temporel / évolution (7) ──────────────────────────────────────────────
    {
        "category": "Temporel / évolution",
        "question": "Quel mois de 2024 a enregistré le plus grand nombre de commandes ?",
        "expected": (
            "doit identifier un mois de 2024 (nom ou numéro) avec le nombre de commandes correspondant"
        ),
    },
    {
        "category": "Temporel / évolution",
        "question": "Quel est le chiffre d'affaires total par année ?",
        "expected": (
            "doit présenter le CA pour chaque année disponible (2023, 2024, 2025) avec les montants en euros"
        ),
    },
    {
        "category": "Temporel / évolution",
        "question": "Compare le CA du premier trimestre 2024 avec celui du quatrième trimestre 2024.",
        "expected": (
            "doit comparer deux montants de CA pour Q1 (jan–mars 2024) et Q4 (oct–déc 2024), "
            "et indiquer lequel est supérieur"
        ),
    },
    {
        "category": "Temporel / évolution",
        "question": "Quelle est l'évolution mensuelle du nombre de commandes en 2024 ?",
        "expected": (
            "doit présenter 12 lignes ou colonnes avec le nombre de commandes pour chaque mois de 2024"
        ),
    },
    {
        "category": "Temporel / évolution",
        "question": "Quel trimestre de 2023 a enregistré le plus de commandes livrées ?",
        "expected": (
            "doit identifier un trimestre (Q1/Q2/Q3/Q4) de 2023 avec le nombre de commandes "
            "ayant le statut 'livré'"
        ),
    },
    {
        "category": "Temporel / évolution",
        "question": "Montre le chiffre d'affaires par mois sur toutes les années pour visualiser la saisonnalité.",
        "expected": (
            "doit présenter le CA pour chaque mois (ou chaque combinaison année-mois) "
            "sur l'ensemble des données, permettant d'observer une tendance saisonnière"
        ),
    },
    {
        "category": "Temporel / évolution",
        "question": "Quel est le chiffre d'affaires total du mois de novembre 2024 ?",
        "expected": (
            "doit mentionner un montant de CA en euros spécifiquement pour novembre 2024"
        ),
    },

    # ── Filtres combinés (6) ──────────────────────────────────────────────────
    {
        "category": "Filtres combinés",
        "question": "Quels clients de Paris ont commandé des produits de la catégorie Électronique ?",
        "expected": (
            "doit lister des noms de clients dont la ville est Paris "
            "et qui ont passé au moins une commande contenant un produit Électronique"
        ),
    },
    {
        "category": "Filtres combinés",
        "question": "Combien de commandes ont été annulées en 2024 ?",
        "expected": (
            "doit mentionner un nombre entier de commandes avec le statut 'annulé' en 2024"
        ),
    },
    {
        "category": "Filtres combinés",
        "question": "Quel est le chiffre d'affaires total en comptant uniquement les commandes livrées ?",
        "expected": (
            "doit mentionner un montant de CA en euros calculé uniquement sur les commandes "
            "avec le statut 'livré'"
        ),
    },
    {
        "category": "Filtres combinés",
        "question": "Quels produits de la catégorie Beauté ont un prix unitaire supérieur à 100 euros ?",
        "expected": (
            "doit lister des produits dont la catégorie est Beauté et le prix_unitaire > 100, "
            "avec les prix correspondants"
        ),
    },
    {
        "category": "Filtres combinés",
        "question": "Quels clients de Lyon ont passé plus de 3 commandes ?",
        "expected": (
            "doit lister des noms de clients dont la ville est Lyon "
            "avec leur nombre de commandes, tous supérieurs à 3"
        ),
    },
    {
        "category": "Filtres combinés",
        "question": "Quel est le panier moyen par ville pour les commandes livrées uniquement ?",
        "expected": (
            "doit présenter plusieurs villes avec leur panier moyen en euros, "
            "calculé uniquement sur les commandes avec le statut 'livré'"
        ),
    },

    # ── Agrégations complexes (5) ─────────────────────────────────────────────
    {
        "category": "Agrégations complexes",
        "question": "Quel est le panier moyen global par commande ?",
        "expected": (
            "doit mentionner un montant moyen en euros par commande "
            "(valeur plausible entre 50€ et 2 000€)"
        ),
    },
    {
        "category": "Agrégations complexes",
        "question": "Quelle est la valeur moyenne d'une ligne de commande par catégorie de produit ?",
        "expected": (
            "doit présenter les 5 catégories avec la valeur moyenne en euros "
            "d'une ligne de commande (quantite × prix_unitaire) pour chacune"
        ),
    },
    {
        "category": "Agrégations complexes",
        "question": "Quel pourcentage des commandes sont annulées ?",
        "expected": (
            "doit mentionner un pourcentage ou ratio de commandes annulées "
            "(valeur attendue autour de 10 %)"
        ),
    },
    {
        "category": "Agrégations complexes",
        "question": "Combien de clients distincts ont passé plus d'une commande ?",
        "expected": (
            "doit mentionner un nombre de clients (sur 200 au total) "
            "ayant passé au moins 2 commandes"
        ),
    },
    {
        "category": "Agrégations complexes",
        "question": "Quel est le nombre moyen de lignes de produits par commande ?",
        "expected": (
            "doit mentionner un nombre moyen de lignes par commande "
            "(valeur plausible entre 1 et 5)"
        ),
    },

    # ── Questions pièges / ambiguës (4) ──────────────────────────────────────
    {
        "category": "Questions pièges / ambiguës",
        "question": "Quel est le meilleur client ?",
        "expected": (
            "doit choisir une interprétation (CA total ou nombre de commandes), "
            "l'expliciter clairement, et donner un nom de client avec la valeur correspondante"
        ),
    },
    {
        "category": "Questions pièges / ambiguës",
        "question": "Combien avons-nous fait de ventes ?",
        "expected": (
            "doit choisir une interprétation (nombre de commandes, nombre de lignes de commande, "
            "ou CA total), l'expliciter, et donner un chiffre cohérent"
        ),
    },
    {
        "category": "Questions pièges / ambiguës",
        "question": "Quels clients sont inactifs ?",
        "expected": (
            "doit définir une hypothèse explicite sur ce qu'est un client 'inactif' "
            "(ex : sans commande depuis X mois) et lister des clients correspondants"
        ),
    },
    {
        "category": "Questions pièges / ambiguës",
        "question": "Quel produit s'est le plus mal vendu ce trimestre ?",
        "expected": (
            "doit interpréter 'ce trimestre' comme Q1 2026 (janvier–mars 2026), "
            "constater qu'il n'y a aucune vente sur cette période (données jusqu'à fin 2025), "
            "et l'expliquer clairement plutôt que de retourner un résultat vide sans contexte"
        ),
    },
]


@dataclass
class Result:
    num: int
    question: str
    category: str
    expected: str
    sql: str = ""
    agent_response: str = ""
    score: Optional[int] = None
    verdict: str = ""
    error: str = ""


def run_question(num: int, q: dict) -> Result:
    result = Result(
        num=num,
        question=q["question"],
        category=q["category"],
        expected=q["expected"],
    )
    try:
        response, sql = answer_with_sql(q["question"])
        result.sql = sql
        result.agent_response = response
    except Exception as e:
        result.error = str(e)
        result.agent_response = f"Erreur inattendue : {e}"
    return result


def judge(client: anthropic.Anthropic, result: Result) -> tuple[int, str]:
    if result.error:
        return 0, f"Erreur technique : {result.error[:80]}"

    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system=[{
            "type": "text",
            "text": JUDGE_SYSTEM,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{
            "role": "user",
            "content": (
                f"Question posée : {result.question}\n\n"
                f"Critères attendus : {result.expected}\n\n"
                f"Réponse de l'agent :\n{result.agent_response}"
            ),
        }],
    )

    text = response.content[0].text.strip()
    try:
        data = json.loads(text)
        score = int(data["score"])
        verdict = str(data["verdict"])
    except (json.JSONDecodeError, KeyError, ValueError):
        m_score = re.search(r'"score"\s*:\s*([012])', text)
        m_verdict = re.search(r'"verdict"\s*:\s*"([^"]+)"', text)
        score = int(m_score.group(1)) if m_score else 0
        verdict = m_verdict.group(1) if m_verdict else f"Erreur parsing : {text[:60]}"

    return max(0, min(2, score)), verdict


def _category_breakdown(results: list[Result]) -> dict[str, dict]:
    breakdown: dict[str, dict] = {}
    for r in results:
        if r.category not in breakdown:
            breakdown[r.category] = {"score": 0, "max": 0}
        if r.score is not None:
            breakdown[r.category]["score"] += r.score
        breakdown[r.category]["max"] += 2
    return breakdown


def generate_report(results: list[Result], dry_run: bool) -> str:
    today = date.today().isoformat()
    scored = [r for r in results if r.score is not None]
    total_score = sum(r.score for r in scored)  # type: ignore[arg-type]
    max_score = len(results) * 2
    pct = round(total_score / max_score * 100, 1) if max_score else 0.0

    lines: list[str] = []

    lines.append(f"# Benchmark SQL Agent — {today}\n")

    if dry_run:
        lines.append("*Mode dry-run — jugement Claude désactivé, scores non calculés.*\n")
    else:
        lines.append(f"**Score global : {total_score}/{max_score} ({pct} %)**\n")

        breakdown = _category_breakdown(results)
        lines.append("## Résultats par catégorie\n")
        lines.append("| Catégorie | Score | Max | Taux |")
        lines.append("|---|---|---|---|")
        for cat, data in breakdown.items():
            cat_pct = round(data["score"] / data["max"] * 100, 1) if data["max"] else 0.0
            lines.append(f"| {cat} | {data['score']} | {data['max']} | {cat_pct} % |")
        lines.append("")

    lines.append("## Détail question par question\n")

    for r in results:
        lines.append(f"### Q{r.num:02d} — {r.category}\n")
        lines.append(f"**Question :** {r.question}\n")
        if not dry_run:
            score_str = f"{r.score}/2" if r.score is not None else "N/A"
            lines.append(f"**Score :** {score_str}\n")
        lines.append(f"**SQL généré :**\n```sql\n{r.sql or 'N/A'}\n```\n")
        lines.append(f"**Réponse agent :**\n\n{r.agent_response}\n")
        if not dry_run:
            lines.append(f"**Verdict juge :** {r.verdict}\n")
        lines.append("---\n")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark de l'agent SQL e-commerce")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Exécute les questions sans appeler le juge Claude (SQL + réponse agent uniquement)",
    )
    args = parser.parse_args()

    client = anthropic.Anthropic()

    mode = "dry-run (juge désactivé)" if args.dry_run else "complet (juge actif)"
    print(f"Benchmark SQL Agent — {len(QUESTIONS)} questions — mode {mode}")
    print()

    results: list[Result] = []

    for i, q in enumerate(QUESTIONS, 1):
        label = q["question"] if len(q["question"]) <= 65 else q["question"][:62] + "..."
        print(f"[Q{i:02d}/{len(QUESTIONS)}] {label}", end="", flush=True)

        result = run_question(i, q)

        if args.dry_run:
            status = "ERREUR" if result.error else "OK"
            print(f"  [{status}]")
        else:
            score, verdict = judge(client, result)
            result.score = score
            result.verdict = verdict
            verdict_short = verdict[:55] + "…" if len(verdict) > 55 else verdict
            print(f"  [{score}/2] {verdict_short}")

        results.append(result)

        if i < len(QUESTIONS):
            time.sleep(SLEEP_BETWEEN_S)

    print()

    if not args.dry_run:
        scored = [r for r in results if r.score is not None]
        total = sum(r.score for r in scored)  # type: ignore[arg-type]
        max_s = len(results) * 2
        pct = round(total / max_s * 100, 1) if max_s else 0.0
        print(f"Score final : {total}/{max_s} ({pct} %)")

    report = generate_report(results, dry_run=args.dry_run)
    report_path = "benchmark_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Rapport exporté : {report_path}")


if __name__ == "__main__":
    main()
