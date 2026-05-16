# Benchmark SQL Agent — 2026-05-16

**Score global : 51/60 (85.0 %)**

## Résultats par catégorie

| Catégorie | Score | Max | Taux |
|---|---|---|---|
| Top/flop simples | 12 | 16 | 75.0 % |
| Temporel / évolution | 13 | 14 | 92.9 % |
| Filtres combinés | 12 | 12 | 100.0 % |
| Agrégations complexes | 8 | 10 | 80.0 % |
| Questions pièges / ambiguës | 6 | 8 | 75.0 % |

## Détail question par question

### Q01 — Top/flop simples

**Question :** Quel est le top 5 clients en chiffre d'affaires total ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT c.id, c.nom, c.email, SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM clients c
JOIN commandes cmd ON cmd.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = cmd.id
WHERE cmd.statut = 'livré'
GROUP BY c.id, c.nom, c.email
ORDER BY ca_total DESC
LIMIT 5;
```

**Réponse agent :**

## 🏆 Top 5 Clients par Chiffre d'Affaires Total

Voici le classement des 5 meilleurs clients, calculé sur la base des **commandes livrées uniquement** :

| Rang | Client | Email | CA Total |
|------|--------|-------|----------|
| 🥇 1 | Stéphane-Marcel Guillon | oetienne@example.org | **33 152,16 €** |
| 🥈 2 | Timothée-Roger Vasseur | zoe03@example.org | **25 276,95 €** |
| 🥉 3 | Élodie Auger-Delahaye | cvasseur@example.net | **25 101,93 €** |
| 4 | Noémi Royer | lecomtehelene@example.net | **21 516,71 €** |
| 5 | Alexandre Traore | patrick32@example.net | **19 047,86 €** |

---

### 📊 Points clés

- 🔝 **Stéphane-Marcel Guillon** se détache nettement avec **33 152 €**, soit environ **31% de plus** que le 2ème client.
- Les **2ème et 3ème** sont très proches avec seulement **175 € d'écart**, ce qui en fait un duo quasi ex-æquo.
- L'ensemble de ces **5 clients représente 124 095,55 €** de chiffre d'affaires cumulé.

> ⚠️ **Note méthodologique** : Ce classement ne prend en compte que les commandes au statut **"livré"**. Les commandes en cours, annulées ou en attente sont exclues du calcul, ce qui reflète le CA réellement encaissé.

**Verdict juge :** Réponse complète : 5 clients nommés avec CA en euros, triés décroissant, méthodologie explicitée.

---

### Q02 — Top/flop simples

**Question :** Quel est le produit le plus vendu en quantité totale ?

**Score :** 1/2

**SQL généré :**
```sql
SELECT p.nom AS produit, SUM(lc.quantite) AS quantite_totale
FROM lignes_commande lc
JOIN produits p ON lc.produit_id = p.id
JOIN commandes c ON lc.commande_id = c.id
WHERE c.statut = 'livré'
GROUP BY p.id, p.nom
ORDER BY quantite_totale DESC
LIMIT 1;
```

**Réponse agent :**

## 🏆 Produit le plus vendu

Le produit **Chemin Vêt-39** est le champion des ventes en volume, avec un total de **154 unités vendues** sur l'ensemble des commandes livrées.

| Produit | Quantité Totale Vendue |
|-------------|----------------------|
| Chemin Vêt-39 | 154 unités |

### 💡 Analyse business

- Cette analyse porte **uniquement sur les commandes au statut "livré"**, ce qui garantit que les chiffres reflètent des ventes réellement concrétisées.
- Le produit **Chemin Vêt-39** se démarque clairement comme le **best-seller en volume**, ce qui peut indiquer :
  - Une forte demande client sur ce référence
  - Un positionnement prix attractif
  - Une bonne disponibilité en stock

> **Recommandation** : Il serait pertinent de s'assurer que ce produit bénéficie d'un **approvisionnement prioritaire** et d'analyser sa **marge contributive** pour vérifier qu'il est également rentable, pas seulement populaire.

**Verdict juge :** Réponse complète mais filtrée sur 'livré' seulement, sans justification explicite de ce choix restrictif.

---

### Q03 — Top/flop simples

**Question :** Quelle catégorie de produits génère le plus de chiffre d'affaires ?

**Score :** 1/2

**SQL généré :**
```sql
SELECT p.categorie, SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM lignes_commande lc
JOIN produits p ON lc.produit_id = p.id
JOIN commandes c ON lc.commande_id = c.id
WHERE c.statut = 'livré'
GROUP BY p.categorie
ORDER BY ca_total DESC
LIMIT 1;
```

**Réponse agent :**

## 📊 Analyse du Chiffre d'Affaires par Catégorie

### Résultat

| Catégorie | Chiffre d'Affaires Total |
|-----------|--------------------------|
| **Vêtements** | **380 651,66 €** |

### 💡 Insight Business

La catégorie **Vêtements** est la **première source de revenus** de l'entreprise, avec un chiffre d'affaires de **380 651,66 €** sur les commandes livrées.

Quelques points notables :

- Ce chiffre est calculé **uniquement sur les commandes effectivement livrées**, ce qui en fait un indicateur fiable du revenu réellement encaissé (hors commandes en cours ou annulées).
- La domination de cette catégorie suggère qu'elle représente probablement le **cœur de l'activité commerciale** et mérite une attention particulière en termes de :
  - **Gestion des stocks** pour éviter les ruptures
  - **Politique tarifaire** et promotions ciblées
  - **Fidélisation** des acheteurs de cette catégorie

### 🔍 Recommandation
Il serait pertinent d'élargir l'analyse à **toutes les catégories** pour mesurer la part relative des Vêtements dans le CA global et identifier d'éventuelles catégories à fort potentiel de croissance.

**Verdict juge :** Catégorie nommée et CA fourni, mais filtre 'commandes livrées' restreint le périmètre sans justification explicite de la question.

---

### Q04 — Top/flop simples

**Question :** Quels sont les 3 produits les moins vendus en quantité ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT p.id, p.nom, p.categorie, SUM(lc.quantite) AS quantite_totale
FROM produits p
LEFT JOIN lignes_commande lc ON p.id = lc.produit_id
LEFT JOIN commandes c ON lc.commande_id = c.id AND c.statut != 'annulé'
GROUP BY p.id, p.nom, p.categorie
ORDER BY quantite_totale ASC
LIMIT 3;
```

**Réponse agent :**

## 📉 Les 3 produits les moins vendus en quantité

Voici les produits ayant enregistré les plus faibles volumes de ventes (hors commandes annulées) :

| Rang | ID | Produit | Catégorie | Quantité vendue |
|------|----|------------------|---------------|-----------------|
| 🥉 1er | 47 | Habiter Éle-47 | Électronique | 106 unités |
| 🥈 2ème | 35 | Vers Spo-35 | Sport | 111 unités |
| 🥇 3ème | 14 | Attacher Spo-14 | Sport | 124 unités |

---

### 💡 Analyse business

- **Habiter Éle-47** est le produit le moins performant avec seulement **106 unités** écoulées, dans la catégorie Électronique qui est pourtant souvent un segment dynamique.
- **La catégorie Sport est surreprésentée** avec 2 produits sur 3 dans ce classement, ce qui peut signaler un **problème structurel** sur cette gamme (prix, visibilité, concurrence).
- L'écart entre le 1er et le 3ème est relativement faible (**18 unités**), ce qui suggère des performances homogènement basses pour ces articles.

### ⚠️ Points d'attention recommandés
> - Envisager des **actions promotionnelles** ciblées sur ces références
> - Analyser si ces produits souffrent d'un **manque de visibilité** ou d'un **problème de pricing**
> - Évaluer la pertinence de **maintenir ces références** au catalogue si la tendance persiste

**Verdict juge :** Réponse complète : 3 produits listés avec quantités, triés du moins au plus vendu, avec contexte clair.

---

### Q05 — Top/flop simples

**Question :** Quel client a passé le plus grand nombre de commandes ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT c.id, c.nom, c.email, COUNT(co.id) AS nombre_commandes
FROM clients c
JOIN commandes co ON co.client_id = c.id
GROUP BY c.id, c.nom, c.email
ORDER BY nombre_commandes DESC
LIMIT 1;
```

**Réponse agent :**

## 🏆 Client le plus fidèle

Le client ayant passé le plus grand nombre de commandes est :

| ID | Nom | Email | Nombre de commandes |
|----|-----|-------|-------------------|
| 12 | Timothée-Roger Vasseur | zoe03@example.org | 15 |

### 📊 Analyse business

**Timothée-Roger Vasseur** se distingue comme le client le plus actif de la base avec **15 commandes** passées à ce jour.

> 💡 **Recommandation** : Ce type de client à haute fréquence d'achat représente un profil VIP à fort potentiel de fidélisation. Il serait pertinent de :
> - L'intégrer dans un **programme de fidélité premium**
> - Lui proposer des **offres exclusives ou anticipées**
> - Analyser ses habitudes d'achat pour mieux cibler les recommandations produits

**Verdict juge :** Réponse complète avec nom du client et nombre de commandes (15), plus analyse pertinente.

---

### Q06 — Top/flop simples

**Question :** Quelle ville génère le plus de chiffre d'affaires total ?

**Score :** 1/2

**SQL généré :**
```sql
SELECT c.ville, SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM clients c
JOIN commandes co ON co.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = co.id
WHERE co.statut = 'livré'
GROUP BY c.ville
ORDER BY ca_total DESC
LIMIT 1;
```

**Réponse agent :**

## 🏆 Ville générant le plus de chiffre d'affaires

| Ville | Chiffre d'affaires total |
|-------|--------------------------|
| **Angers** | **130 216,45 €** |

### 📊 Analyse

**Angers** se démarque comme la ville la plus performante en termes de chiffre d'affaires, avec **130 216,45 €** générés sur les commandes livrées.

### 💡 Points de contexte
- Ce chiffre est calculé **uniquement sur les commandes au statut "livré"**, ce qui reflète le chiffre d'affaires **réellement encaissé** (hors commandes en cours, annulées ou en attente).
- Cela peut s'expliquer par une **concentration plus élevée de clients** à Angers, des **commandes de plus grande valeur**, ou une **fréquence d'achat** supérieure aux autres villes.

### 🔍 Recommandations
- Il serait pertinent de **comparer Angers aux autres villes** pour mesurer l'écart et identifier d'éventuels marchés à fort potentiel sous-exploités.
- Analyser le **nombre de clients et le panier moyen** à Angers permettrait de mieux comprendre les facteurs de cette performance.

**Verdict juge :** Ville et CA fournis, mais filtre sur statut 'livré' non demandé peut fausser le résultat total.

---

### Q07 — Top/flop simples

**Question :** Quel est le produit le plus cher du catalogue ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT id, nom, categorie, prix_unitaire
FROM produits
ORDER BY prix_unitaire DESC
LIMIT 1;
```

**Réponse agent :**

## Produit le plus cher du catalogue

Le produit le plus onéreux du catalogue est :

| ID | Nom | Catégorie | Prix Unitaire |
|----|-----|-----------|---------------|
| 2 | Descendre Bea-2 | Beauté | **492,01 €** |

### 💡 Insight Business

Le produit le plus cher appartient à la catégorie **Beauté**, avec un prix unitaire de **492,01 €**. Ce positionnement haut de gamme dans cette catégorie peut indiquer une stratégie **premium** sur le segment beauté. Il serait pertinent d'analyser :
- Le **volume de ventes** de ce produit pour évaluer son attractivité malgré son prix élevé
- Sa **marge** par rapport aux autres produits de la même catégorie
- Son impact sur le **panier moyen** des clients qui l'achètent

**Verdict juge :** Réponse complète avec nom du produit et prix unitaire en euros clairement indiqués.

---

### Q08 — Top/flop simples

**Question :** Quels sont les 5 produits avec le CA total le plus élevé ?

**Score :** 1/2

**SQL généré :**
```sql
SELECT p.id, p.nom, p.categorie, SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM produits p
JOIN lignes_commande lc ON lc.produit_id = p.id
JOIN commandes c ON c.id = lc.commande_id
WHERE c.statut = 'livré'
GROUP BY p.id, p.nom, p.categorie
ORDER BY ca_total DESC
LIMIT 5;
```

**Réponse agent :**

## Top 5 des produits par Chiffre d'Affaires

Voici les 5 produits ayant généré le chiffre d'affaires le plus élevé, calculé sur l'ensemble des **commandes livrées** :

| Rang | Produit | Catégorie | CA Total |
|------|---------|-----------|----------|
| 🥇 1 | Amener Vêt-30 | Vêtements | 69 238,80 € |
| 🥈 2 | Descendre Bea-2 | Beauté | 57 457,70 € |
| 🥉 3 | Bon Mai-12 | Maison | 56 248,34 € |
| 4 | Claire Bea-28 | Beauté | 54 542,27 € |
| 5 | Or Éle-38 | Électronique | 53 301,96 € |

**CA cumulé du Top 5 : 290 789,07 €**

---

### 💡 Points clés

- 🏆 **Amener Vêt-30** (Vêtements) domine nettement avec **69 238,80 €**, soit un écart de +20% par rapport au 2ème.
- 📦 La catégorie **Beauté** place **2 produits** dans le top 5 (rangs 2 et 4), ce qui en fait la catégorie la plus représentée.
- Les 5 produits proviennent de **4 catégories différentes**, témoignant d'une diversification des revenus.
- Les écarts entre le rang 2 et le rang 5 sont relativement faibles (~4 000 €), indiquant une **compétition serrée** dans le mid-range.

> ⚠️ *Note : Ces chiffres excluent les commandes annulées ou en cours, reflétant uniquement le CA effectivement encaissé (statut "livré").*

**Verdict juge :** Réponse bien structurée mais filtre sur 'livré' seulement, sans confirmer que c'est l'interprétation attendue pour le CA total.

---

### Q09 — Temporel / évolution

**Question :** Quel mois de 2024 a enregistré le plus grand nombre de commandes ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT strftime('%m', date_commande) AS mois,
       COUNT(*) AS nombre_commandes
FROM commandes
WHERE strftime('%Y', date_commande) = '2024'
GROUP BY mois
ORDER BY nombre_commandes DESC
LIMIT 1;
```

**Réponse agent :**

## Analyse des commandes 2024 par mois

### Résultat

| Mois | Nombre de commandes |
|------|-------------------|
| Décembre 2024 | **70 commandes** |

### Interprétation

Le mois de **décembre 2024** est le mois ayant enregistré le **plus grand volume de commandes** sur l'année, avec **70 commandes** passées.

### Contexte business

Ce pic en décembre est cohérent avec les tendances habituelles du commerce, notamment :
- 🎄 **Les achats de fin d'année** (fêtes de Noël, Nouvel An)
- 🛍️ **Les promotions saisonnières** (Black Friday en retard, soldes hivernales)
- 📦 **L'effet des cadeaux** et des achats groupés en famille

> **Recommandation :** Il serait pertinent de comparer ce chiffre avec décembre des années précédentes pour déterminer s'il s'agit d'une tendance récurrente ou d'une performance exceptionnelle, et ainsi anticiper les ressources nécessaires (stocks, logistique, service client) pour décembre 2025.

**Verdict juge :** Réponse complète : mois identifié (décembre 2024) avec nombre de commandes (70).

---

### Q10 — Temporel / évolution

**Question :** Quel est le chiffre d'affaires total par année ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    strftime('%Y', c.date_commande) AS annee,
    SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM commandes c
JOIN lignes_commande lc ON lc.commande_id = c.id
WHERE c.statut = 'livré'
GROUP BY annee
ORDER BY annee
LIMIT 20;
```

**Réponse agent :**

## Chiffre d'affaires total par année

Voici l'évolution du chiffre d'affaires sur les trois dernières années, basée uniquement sur les **commandes livrées** :

| Année | Chiffre d'affaires |
|-------|-------------------|
| 2023 | 414 436,77 € |
| 2024 | 467 580,77 € |
| 2025 | 496 693,18 € |

### 📈 Analyse

- **Croissance 2023 → 2024** : +53 144 € soit une hausse de **+12,8%**
- **Croissance 2024 → 2025** : +29 112 € soit une hausse de **+6,2%**
- **CA cumulé sur 3 ans** : **1 378 710,72 €**

### 💡 Points de contexte

- La tendance est **globalement positive** avec une croissance continue d'une année sur l'autre.
- Le ralentissement de la croissance entre 2024 et 2025 (+6,2% vs +12,8%) mérite attention : il peut s'expliquer par une **année 2025 encore en cours** (données partielles), ou par un essoufflement réel de la dynamique commerciale.
- Ces chiffres n'incluent **que les commandes livrées**, ce qui en fait une mesure fiable du CA réellement encaissé, excluant les commandes annulées ou en attente.

**Verdict juge :** Réponse complète avec les 3 années, montants en euros, analyses pertinentes et précision sur le périmètre retenu.

---

### Q11 — Temporel / évolution

**Question :** Compare le CA du premier trimestre 2024 avec celui du quatrième trimestre 2024.

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    'Q1 2024' AS trimestre,
    SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM commandes c
JOIN lignes_commande lc ON lc.commande_id = c.id
WHERE c.statut = 'livré'
  AND c.date_commande >= '2024-01-01'
  AND c.date_commande < '2024-04-01'

UNION ALL

SELECT
    'Q4 2024' AS trimestre,
    SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM commandes c
JOIN lignes_commande lc ON lc.commande_id = c.id
WHERE c.statut = 'livré'
  AND c.date_commande >= '2024-10-01'
  AND c.date_commande < '2025-01-01'
```

**Réponse agent :**

## Comparaison du CA : Q1 2024 vs Q4 2024

### Résultats

| Trimestre | Chiffre d'Affaires | Variation |
|-----------|-------------------|-----------|
| Q1 2024 | 72 045,71 € | — |
| Q4 2024 | 203 751,59 € | **+131 705,88 €** |

### Analyse

Le quatrième trimestre 2024 affiche un chiffre d'affaires **2,8 fois supérieur** à celui du premier trimestre, soit une **progression de +183 %** sur l'année.

**Points clés à retenir :**

- 📈 **Croissance très marquée** entre le début et la fin d'année, ce qui suggère une **forte saisonnalité** ou une **montée en puissance commerciale** significative au cours de l'année 2024.
- 🎄 Le Q4 bénéficie classiquement des **achats de fin d'année** (Black Friday, fêtes de Noël), ce qui peut expliquer en partie ce pic.
- ⚠️ L'écart important entre les deux trimestres mérite d'être **contextualisé** : s'agit-il d'une tendance structurelle ou d'un effet ponctuel (gros contrats, campagnes promotionnelles) ?

> **Recommandation :** Il serait pertinent d'analyser les trimestres intermédiaires (Q2 et Q3) pour déterminer si la croissance est **progressive et régulière** ou concentrée sur le dernier trimestre.

**Verdict juge :** Réponse complète avec les deux CA, la comparaison claire et Q4 > Q1 bien identifié.

---

### Q12 — Temporel / évolution

**Question :** Quelle est l'évolution mensuelle du nombre de commandes en 2024 ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    strftime('%m', c.date_commande) AS mois,
    COUNT(c.id) AS nombre_commandes
FROM commandes c
WHERE strftime('%Y', c.date_commande) = '2024'
GROUP BY strftime('%m', c.date_commande)
ORDER BY mois;
```

**Réponse agent :**

## Évolution mensuelle des commandes en 2024

Voici le détail mois par mois du nombre de commandes enregistrées en 2024 :

| Mois | Libellé | Nombre de commandes | Évolution vs mois précédent |
|------|---------|--------------------|-----------------------------|
| 01 | Janvier | 13 | — |
| 02 | Février | 23 | +10 (+76,9%) |
| 03 | Mars | 17 | -6 (-26,1%) |
| 04 | Avril | 10 | -7 (-41,2%) |
| 05 | Mai | 21 | +11 (+110,0%) |
| 06 | Juin | 19 | -2 (-9,5%) |
| 07 | Juillet | 20 | +1 (+5,3%) |
| 08 | Août | 25 | +5 (+25,0%) |
| 09 | Septembre | 18 | -7 (-28,0%) |
| 10 | Octobre | 27 | +9 (+50,0%) |
| 11 | Novembre | 35 | +8 (+29,6%) |
| 12 | Décembre | 70 | +35 (+100,0%) |

**Total 2024 : 298 commandes**

---

### 📊 Principaux enseignements

- 📈 **Tendance générale haussière** sur l'année, avec une accélération très marquée en fin d'année.
- 🔴 **Point bas en avril** (10 commandes) — creux notable à surveiller pour 2025.
- 🚀 **Décembre est le mois record** avec 70 commandes, soit **+100% vs novembre** et plus du **double de la moyenne annuelle** (~25 commandes/mois). Cela reflète probablement un fort **effet saisonnier lié aux fêtes de fin d'année**.
- 📅 **Le second semestre est nettement plus dynamique** que le premier (215 vs 103 commandes), ce qui suggit une saisonnalité structurelle à intégrer dans les prévisions et la gestion des stocks.

**Verdict juge :** Réponse complète avec 12 mois, évolution mensuelle, total et analyse pertinente.

---

### Q13 — Temporel / évolution

**Question :** Quel trimestre de 2023 a enregistré le plus de commandes livrées ?

**Score :** 1/2

**SQL généré :**
```sql
SELECT
    CASE
        WHEN CAST(strftime('%m', date_commande) AS INTEGER) BETWEEN 1 AND 3 THEN 'T1 2023'
        WHEN CAST(strftime('%m', date_commande) AS INTEGER) BETWEEN 4 AND 6 THEN 'T2 2023'
        WHEN CAST(strftime('%m', date_commande) AS INTEGER) BETWEEN 7 AND 9 THEN 'T3 2023'
        ELSE 'T4 2023'
    END AS trimestre,
    COUNT(*) AS nb_commandes_livrees
FROM commandes
WHERE statut = 'livré'
  AND strftime('%Y', date_commande) = '2023'
GROUP BY trimestre
ORDER BY nb_commandes_livrees DESC
LIMIT 1;
```

**Réponse agent :**

## Analyse des commandes livrées en 2023

### Résultat

| Trimestre | Nombre de commandes livrées |
|-----------|----------------------------|
| **T4 2023** | **84** |

### Conclusion

Le **4ème trimestre 2023 (octobre - décembre)** est le trimestre ayant enregistré le plus grand nombre de commandes livrées, avec **84 livraisons**.

### Contexte business

Ce résultat est cohérent avec les tendances commerciales habituelles : le T4 concentre généralement une forte activité en raison des **pics saisonniers** liés aux événements commerciaux majeurs tels que :
- 🛍️ **Black Friday / Cyber Monday** (novembre)
- 🎄 **Achats de fin d'année / fêtes de Noël** (décembre)

> **Recommandation** : Il serait pertinent de comparer ce chiffre avec les autres trimestres pour mesurer l'écart de performance et anticiper les besoins logistiques en T4 2024 (stocks, ressources de livraison, service client).

**Verdict juge :** Identifie T4 2023 avec 84 commandes mais n'affiche pas les autres trimestres pour comparer.

---

### Q14 — Temporel / évolution

**Question :** Montre le chiffre d'affaires par mois sur toutes les années pour visualiser la saisonnalité.

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    strftime('%m', c.date_commande) AS mois,
    strftime('%Y', c.date_commande) AS annee,
    SUM(lc.quantite * lc.prix_unitaire) AS ca_total,
    COUNT(DISTINCT c.id) AS nb_commandes
FROM commandes c
JOIN lignes_commande lc ON lc.commande_id = c.id
WHERE c.statut = 'livré'
GROUP BY mois, annee
ORDER BY annee, mois
LIMIT 20;
```

**Réponse agent :**

## Chiffre d'affaires mensuel – Analyse de la saisonnalité

### Tableau détaillé

| Mois | 2023 – CA (€) | 2023 – Commandes | 2024 – CA (€) | 2024 – Commandes |
|------|--------------|-----------------|--------------|-----------------|
| Janvier | 22 912,62 | 10 | 20 087,44 | 9 |
| Février | 29 328,50 | 12 | 36 561,21 | 15 |
| Mars | 48 914,30 | 19 | 15 397,06 | 12 |
| Avril | 6 789,37 | 5 | 17 695,55 | 7 |
| Mai | 16 505,85 | 8 | 27 519,07 | 14 |
| Juin | 33 831,92 | 17 | 38 901,65 | 17 |
| Juillet | 17 095,00 | 10 | 36 300,62 | 16 |
| Août | 36 919,73 | 19 | 48 468,35 | 19 |
| Septembre | 39 203,64 | 14 | *(données à venir)* | – |
| Octobre | 23 865,87 | 12 | *(données à venir)* | – |
| Novembre | 70 808,42 | 31 | *(données à venir)* | – |
| Décembre | 68 261,55 | 41 | *(données à venir)* | – |

---

### 📊 Enseignements clés

#### 🔴 Points bas (creux saisonniers)
- **Avril 2023** est le mois le plus faible de l'année avec seulement **6 789 €** et 5 commandes — un creux très marqué après le pic de mars.
- **Janvier–Février** démarrent l'année doucement (~22–29k€).

#### 🟢 Pics saisonniers identifiés
- **Novembre–Décembre 2023** dominent très largement : **70 808 €** et **68 261 €**, soit les **2 meilleurs mois de l'année** — effet Black Friday / fêtes de fin d'année très net.
- **Mars 2023** constitue un **pic de printemps** (48 914 €), qui ne se répète pas en 2024 (15 397 €) → potentiellement lié à une commande exceptionnelle.
- **Août** est régulièrement fort : **36 919 €** en 2023 et **48 468 €** en 2024 → pic estival cohérent.

#### 📈 Tendance 2024 vs 2023
Sur les mois comparables (janvier à août) :
- 2023 : **251 272 €** de CA cumulé
- 2024 : **240 930 €** de CA cumulé *(légèrement en retrait, mais l'absence du pic de mars 2023 explique l'écart)*
- En excluant mars, la tendance 2024 est **en progression** (+17% sur le reste des mois).

---

### 💡 Recommandations

| Action | Contexte |
|--------|----------|
| **Renforcer les stocks/équipes en nov-déc** | Pic de fin d'année très structurel |
| **Animer commercialement avril** | Creux récurrent à stimuler (promotions, campagnes) |
| **Capitaliser sur août** | Mois d'été performant et en croissance |
| **Investiguer le pic mars 2023** | Comprendre s'il est reproductible ou exceptionnel |

**Verdict juge :** Réponse complète avec CA par mois et année, saisonnalité analysée, insights pertinents et recommandations.

---

### Q15 — Temporel / évolution

**Question :** Quel est le chiffre d'affaires total du mois de novembre 2024 ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM lignes_commande lc
JOIN commandes c ON lc.commande_id = c.id
WHERE c.statut = 'livré'
  AND strftime('%Y-%m', c.date_commande) = '2024-11'
```

**Réponse agent :**

## Chiffre d'affaires de novembre 2024

Le chiffre d'affaires total réalisé sur le mois de **novembre 2024** s'élève à :

> # 💰 64 336,43 €

### Contexte & précisions

Ce montant est calculé sur la base des **commandes effectivement livrées** en novembre 2024, ce qui reflète le chiffre d'affaires **réellement encaissable** (les commandes en attente ou annulées sont exclues du calcul).

> ⚠️ **Note analytique** : Si l'on souhaitait une vision plus complète, il pourrait être pertinent de comparer ce chiffre avec :
> - Le mois d'**octobre 2024** (évolution mensuelle)
> - **Novembre 2023** (évolution annuelle / saisonnalité)
> - L'**objectif budgétaire** fixé pour ce mois

**Verdict juge :** Réponse complète avec montant précis en euros pour novembre 2024, méthodologie explicitée.

---

### Q16 — Filtres combinés

**Question :** Quels clients de Paris ont commandé des produits de la catégorie Électronique ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT DISTINCT c.id, c.nom, c.email
FROM clients c
JOIN commandes cmd ON cmd.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = cmd.id
JOIN produits p ON p.id = lc.produit_id
WHERE c.ville = 'Paris'
  AND p.categorie = 'Électronique'
LIMIT 20;
```

**Réponse agent :**

## Clients parisiens ayant commandé des produits Électronique

Sur l'ensemble de la base clients, **5 clients domiciliés à Paris** ont passé au moins une commande incluant un produit de la catégorie **Électronique** :

| ID | Nom | Email |
|----|-----|-------|
| 15 | Gilles Joly | noemiguilbert@example.net |
| 76 | Pénélope du Leroux | qlebreton@example.org |
| 93 | Théodore Blot | francoisgrenier@example.com |
| 95 | Marianne de De Oliveira | bgautier@example.com |
| 152 | Constance Legrand-Pichon | jacqueline46@example.net |

### 💡 Points business à retenir

- **Paris** représente un segment géographique clé à cibler pour les campagnes marketing sur l'électronique.
- Ces **5 clients identifiés** constituent une audience qualifiée pour des actions de **fidélisation** (offres exclusives, avant-premières produits, programme de fidélité).
- Il serait pertinent d'**analyser le panier moyen** et la **fréquence d'achat** de ces clients pour prioriser les efforts commerciaux sur les profils les plus rentables.
- Une campagne d'**email marketing ciblée** sur ces contacts pourrait être envisagée pour promouvoir les nouvelles références Électronique.

**Verdict juge :** Réponse complète avec noms, IDs, emails des clients parisiens ayant commandé en Électronique.

---

### Q17 — Filtres combinés

**Question :** Combien de commandes ont été annulées en 2024 ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT COUNT(*) AS nb_commandes_annulees
FROM commandes
WHERE statut = 'annulé'
AND strftime('%Y', date_commande) = '2024';
```

**Réponse agent :**

## Commandes annulées en 2024

En 2024, **19 commandes** ont été annulées.

### Contexte business
Ce chiffre mérite d'être mis en perspective :
- **Taux d'annulation** : il serait utile de le comparer au nombre total de commandes passées en 2024 pour évaluer le pourcentage d'annulation.
- **Tendance** : une comparaison avec les années précédentes permettrait de déterminer si ce niveau d'annulation est en hausse, en baisse ou stable.
- **Causes potentielles** : identifier les raisons des annulations (rupture de stock, délais de livraison, insatisfaction client, etc.) pourrait aider à mettre en place des actions correctives.

> 💡 **Recommandation** : Croiser ces données avec les motifs d'annulation et la période de l'année pourrait révéler des patterns exploitables pour réduire ce taux.

**Verdict juge :** Réponse correcte : 19 commandes annulées en 2024, nombre entier clair avec contexte utile.

---

### Q18 — Filtres combinés

**Question :** Quel est le chiffre d'affaires total en comptant uniquement les commandes livrées ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM lignes_commande lc
JOIN commandes c ON lc.commande_id = c.id
WHERE c.statut = 'livré';
```

**Réponse agent :**

## Chiffre d'affaires sur commandes livrées

Le chiffre d'affaires généré **uniquement sur les commandes effectivement livrées** s'élève à :

| Indicateur | Montant |
|---|---|
| **CA Total (commandes livrées)** | **1 378 710,72 €** |

### 💡 Analyse business

Ce montant représente le **revenu réellement concrétisé**, c'est-à-dire les ventes pour lesquelles la livraison a bien été effectuée. Il s'agit d'un indicateur fiable pour évaluer la **performance commerciale réelle**, car il exclut :

- ❌ Les commandes en cours de traitement
- ❌ Les commandes en attente ou en transit
- ❌ Les commandes annulées ou remboursées

> **À noter** : Ce chiffre peut différer du CA total (toutes commandes confondues). Il est recommandé de comparer ces deux valeurs pour mesurer le **taux de concrétisation des ventes** et identifier d'éventuels points de blocage dans le processus de livraison.

**Verdict juge :** Réponse complète avec montant précis en euros filtré sur commandes livrées, analyse claire et pertinente.

---

### Q19 — Filtres combinés

**Question :** Quels produits de la catégorie Beauté ont un prix unitaire supérieur à 100 euros ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT id, nom, categorie, prix_unitaire
FROM produits
WHERE categorie = 'Beauté'
  AND prix_unitaire > 100
ORDER BY prix_unitaire DESC
LIMIT 20;
```

**Réponse agent :**

## Produits Beauté à prix unitaire supérieur à 100 €

Voici les **8 produits** de la catégorie **Beauté** dont le prix unitaire dépasse 100 € :

| ID | Nom du produit | Catégorie | Prix unitaire |
|----|----------------|-----------|--------------|
| 2 | Descendre Bea-2 | Beauté | 492,01 € |
| 28 | Claire Bea-28 | Beauté | 442,65 € |
| 1 | Obtenir Bea-1 | Beauté | 353,25 € |
| 50 | Instant Bea-50 | Beauté | 220,11 € |
| 45 | But Bea-45 | Beauté | 202,84 € |
| 46 | Mien Bea-46 | Beauté | 168,92 € |
| 4 | Marchand Bea-4 | Beauté | 153,19 € |
| 9 | Repas Bea-9 | Beauté | 109,26 € |

### 📊 Quelques repères business

- **Prix le plus élevé** : 492,01 € (Descendre Bea-2)
- **Prix le plus bas** (dans cette sélection) : 109,26 € (Repas Bea-9)
- **Prix moyen** de ces produits premium : ~**268 €**

> 💡 **Analyse** : On observe une forte dispersion des prix, avec un écart de près de **383 €** entre le produit le plus cher et le moins cher de cette sélection. Les 3 premiers produits (> 350 €) constituent un segment **haut de gamme** clairement distinct des 5 autres, qui se positionnent dans une fourchette plus intermédiaire (100–220 €). Ces produits premium méritent une attention particulière en termes de **gestion des stocks et de stratégie promotionnelle**.

**Verdict juge :** Réponse complète : 8 produits Beauté avec prix > 100€, bien présentés avec analyses pertinentes.

---

### Q20 — Filtres combinés

**Question :** Quels clients de Lyon ont passé plus de 3 commandes ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT c.id, c.nom, c.email, COUNT(co.id) AS nombre_commandes
FROM clients c
JOIN commandes co ON co.client_id = c.id
WHERE c.ville = 'Lyon'
GROUP BY c.id, c.nom, c.email
HAVING COUNT(co.id) > 3
ORDER BY nombre_commandes DESC
LIMIT 20;
```

**Réponse agent :**

## Clients de Lyon avec plus de 3 commandes

L'analyse révèle **5 clients lyonnais** particulièrement actifs, ayant passé plus de 3 commandes. Ce sont des profils à fort potentiel de fidélisation :

| ID | Nom | Email | Nombre de commandes |
|----|-----|-------|:-------------------:|
| 68 | François Perret Le Turpin | rpichon@example.org | 7 |
| 157 | Thomas Pereira | ruizsimone@example.com | 6 |
| 7 | Julie Bertrand du Regnier | hoareauedouard@example.net | 5 |
| 50 | Emmanuelle Torres | corinne74@example.org | 5 |
| 138 | Victoire-Clémence Cohen | vbarre@example.net | 4 |

### 💡 Points clés

- **François Perret Le Turpin** est le client le plus engagé avec **7 commandes**, soit presque le double du seuil minimal.
- **2 clients** se situent à 5 commandes (Julie Bertrand du Regnier et Emmanuelle Torres).
- Le segment représente un **noyau dur de clients fidèles à Lyon**, idéal pour des actions de rétention ou de programme de fidélité.

### 📌 Recommandations business
> Ces 5 clients constituent une cible prioritaire pour des offres exclusives (remises VIP, avant-premières, programme de parrainage) afin de maximiser leur **valeur vie client (LTV)** et encourager le bouche-à-oreille sur la région lyonnaise.

**Verdict juge :** Réponse complète : noms, IDs, emails, nb commandes > 3, ville Lyon, 5 clients listés correctement.

---

### Q21 — Filtres combinés

**Question :** Quel est le panier moyen par ville pour les commandes livrées uniquement ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    c.ville,
    COUNT(DISTINCT co.id) AS nb_commandes,
    ROUND(SUM(lc.quantite * lc.prix_unitaire) / COUNT(DISTINCT co.id), 2) AS panier_moyen
FROM clients c
JOIN commandes co ON co.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = co.id
WHERE co.statut = 'livré'
GROUP BY c.ville
ORDER BY panier_moyen DESC
LIMIT 20;
```

**Réponse agent :**

## Panier moyen par ville — Commandes livrées

### Résultats

| Ville | Nb commandes livrées | Panier moyen |
|---|---|---|
| **Dijon** | 29 | **2 552,92 €** |
| **Nantes** | 34 | **2 549,37 €** |
| Nice | 12 | 2 462,03 € |
| Angers | 54 | 2 411,42 € |
| Montpellier | 50 | 2 362,89 € |
| Reims | 30 | 2 346,02 € |
| Toulouse | 46 | 2 236,12 € |
| Lyon | 28 | 2 227,91 € |
| Rennes | 42 | 2 177,83 € |
| Strasbourg | 34 | 2 144,55 € |
| Grenoble | 31 | 2 123,24 € |
| Bordeaux | 52 | 2 098,85 € |
| Marseille | 48 | 2 076,82 € |
| Saint-Étienne | 28 | 1 937,12 € |
| Nîmes | 43 | 1 922,01 € |
| Le Havre | 8 | 1 890,88 € |
| Toulon | 22 | 1 880,02 € |
| Lille | 11 | 1 809,90 € |
| Villeurbanne | 12 | 1 688,14 € |
| **Paris** | 19 | **1 678,83 €** |

---

### 📊 Analyse business

**Écart significatif entre villes** : le panier moyen varie du simple au double entre **Dijon** (2 552 €) et **Paris** (1 678 €), soit un écart de près de **+52%**.

**Points clés à retenir :**

- 🥇 **Dijon et Nantes** se distinguent avec les paniers les plus élevés (> 2 550 €), malgré un volume de commandes modéré (~30 commandes).
- 📦 **Angers, Montpellier et Bordeaux** combinent un **fort volume** (50+ commandes) et un **bon panier moyen** (> 2 000 €) → ce sont les marchés les plus contributifs en chiffre d'affaires.
- ⚠️ **Paris** affiche paradoxalement le **panier moyen le plus faible** (1 678 €) avec seulement 19 commandes livrées — à surveiller : cela peut refléter des commandes plus fragmentées ou une clientèle différente.
- 📍 **Le Havre et Lille** ont peu de commandes livrées (8 et 11), ce qui peut fragiliser la fiabilité statistique de leur panier moyen.

> **Recommandation** : Investiguer les marchés à fort volume mais panier moyen sous 2 000 € (Nîmes, Marseille) pour identifier des leviers d'**upsell ou cross-sell**.

**Verdict juge :** Réponse complète et correcte : plusieurs villes, panier moyen en euros, filtre sur commandes livrées, avec analyse pertinente.

---

### Q22 — Agrégations complexes

**Question :** Quel est le panier moyen global par commande ?

**Score :** 1/2

**SQL généré :**
```sql
SELECT
    ROUND(SUM(lc.quantite * lc.prix_unitaire) * 1.0 / COUNT(DISTINCT lc.commande_id), 2) AS panier_moyen
FROM lignes_commande lc
JOIN commandes c ON c.id = lc.commande_id
WHERE c.statut != 'annulé';
```

**Réponse agent :**

## Panier Moyen Global par Commande

### Résultat

| Indicateur | Valeur |
|---|---|
| 🛒 Panier moyen par commande | **2 257,36 €** |

### Analyse

Le panier moyen global s'établit à **2 257,36 €** par commande, calculé sur l'ensemble des commandes **hors annulations**.

### Points de contexte

- **Périmètre** : Seules les commandes avec un statut actif (hors "annulé") sont prises en compte, ce qui garantit une mesure représentative du chiffre d'affaires réel.
- **Calcul** : Il s'agit du rapport entre le **chiffre d'affaires total** (quantités × prix unitaires) et le **nombre de commandes distinctes**.

### Utilisation business

Ce KPI est fondamental pour :
- 📈 **Suivre la performance commerciale** dans le temps (évolution mensuelle/trimestrielle)
- 🎯 **Fixer des objectifs** d'upselling ou cross-selling pour augmenter ce panier
- 🔍 **Segmenter** par client, région ou catégorie produit pour identifier les leviers de croissance
- ⚖️ **Benchmarker** par rapport aux standards du secteur

> 💡 Un panier de **2 257 €** suggère une activité **B2B** ou à forte valeur unitaire. Il serait pertinent de le ventiler par segment client ou famille de produits pour affiner l'analyse.

**Verdict juge :** Valeur hors plage attendue (2257€ > 2000€), mais réponse structurée avec méthodologie claire.

---

### Q23 — Agrégations complexes

**Question :** Quelle est la valeur moyenne d'une ligne de commande par catégorie de produit ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT p.categorie, AVG(lc.quantite * lc.prix_unitaire) AS valeur_moyenne_ligne
FROM lignes_commande lc
JOIN produits p ON lc.produit_id = p.id
GROUP BY p.categorie
ORDER BY valeur_moyenne_ligne DESC
LIMIT 20;
```

**Réponse agent :**

## Valeur moyenne d'une ligne de commande par catégorie de produit

### Résultats

| Catégorie | Valeur moyenne d'une ligne |
|---------------|---------------------------|
| 🏅 Sport | 981,65 € |
| 👗 Vêtements | 757,09 € |
| 💄 Beauté | 745,93 € |
| 🏠 Maison | 705,85 € |
| 💻 Électronique | 638,12 € |

### Analyse business

La valeur moyenne d'une ligne de commande représente le montant typique engagé par un client lors de l'achat d'un produit (quantité × prix unitaire). Voici les points clés :

- 🥇 **Sport est en tête** avec **981,65 €** par ligne, soit **54 % de plus** que l'Électronique. Cela peut s'expliquer par des achats en quantité (équipements, consommables) ou des produits à prix élevé.

- 📊 **Vêtements, Beauté et Maison** se situent dans une fourchette resserrée entre **706 € et 757 €**, suggérant des comportements d'achat similaires.

- 💡 **L'Électronique**, bien que souvent associée à des produits coûteux, affiche la valeur la **plus faible** (638 €), ce qui peut indiquer des achats unitaires sans multiplication des quantités.

### Recommandations

> **Levier de croissance** : L'Électronique, malgré son potentiel de valeur élevée, sous-performe — des stratégies de **vente croisée** (accessoires, garanties) pourraient augmenter significativement la valeur par ligne. La catégorie Sport, quant à elle, mérite d'être analysée pour comprendre et **reproduire ses facteurs de succès** sur les autres catégories.

**Verdict juge :** Réponse complète avec les 5 catégories, calcul quantité×prix_unitaire correct et analyse pertinente.

---

### Q24 — Agrégations complexes

**Question :** Quel pourcentage des commandes sont annulées ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    COUNT(CASE WHEN statut = 'annulé' THEN 1 END) * 100.0 / COUNT(*) AS pourcentage_annulees
FROM commandes;
```

**Réponse agent :**

## Taux d'annulation des commandes

Sur l'ensemble des commandes enregistrées, **9,13%** d'entre elles sont annulées.

| Indicateur | Valeur |
|---|---|
| Taux d'annulation | **9,13 %** |

### 📊 Analyse business

Ce taux d'annulation de **~9%** mérite attention :

- **Seuil d'alerte** : Dans la plupart des secteurs e-commerce/retail, un taux d'annulation supérieur à **5-10%** est considéré comme préoccupant.
- **Impact financier** : Chaque commande annulée représente un manque à gagner potentiel, ainsi que des coûts opérationnels (traitement, service client, remboursement).
- **Pistes d'investigation** : Il serait pertinent d'analyser les causes d'annulation — délais de livraison, ruptures de stock, insatisfaction prix — afin de mettre en place des actions correctives ciblées.

> 💡 **Recommandation** : Croiser ce taux avec la période (mois/trimestre) et les catégories de produits pour identifier d'éventuels pics ou segments à risque.

**Verdict juge :** Réponse correcte avec 9,13% (~10% attendu), bien présentée avec analyse business pertinente.

---

### Q25 — Agrégations complexes

**Question :** Combien de clients distincts ont passé plus d'une commande ?

**Score :** 1/2

**SQL généré :**
```sql
SELECT COUNT(*) AS nb_clients_multi_commandes
FROM (
    SELECT client_id
    FROM commandes
    WHERE statut != 'annulé'
    GROUP BY client_id
    HAVING COUNT(id) > 1
) AS sous_requete
```

**Réponse agent :**

## Clients ayant passé plusieurs commandes

Sur l'ensemble de la base de données, **161 clients distincts** ont passé **plus d'une commande** (en excluant les commandes annulées).

### Contexte business

Ce chiffre est un indicateur clé de la **fidélisation client** (rétention). Ces 161 clients représentent votre base de clients récurrents, c'est-à-dire ceux qui ont effectué au moins un **réachat**.

Quelques pistes d'analyse complémentaires à envisager :
- 📊 **Quel pourcentage** cela représente-t-il par rapport au nombre total de clients actifs ?
- 🔁 **Quelle est la distribution** du nombre de commandes par client (2 commandes, 3 commandes, etc.) ?
- 💰 **Quelle est la valeur moyenne** des commandes des clients fidèles vs. les nouveaux clients ?
- 📈 **Évolution dans le temps** : ce chiffre progresse-t-il d'un mois sur l'autre ?

Ces clients multi-commandes sont généralement les plus rentables et méritent une attention particulière dans votre stratégie de **fidélisation et de rétention**.

**Verdict juge :** Réponse plausible (161 clients) mais exclut les commandes annulées sans que la question le demande, ce qui peut fausser le chiffre.

---

### Q26 — Agrégations complexes

**Question :** Quel est le nombre moyen de lignes de produits par commande ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT ROUND(CAST(COUNT(lc.id) AS FLOAT) / COUNT(DISTINCT lc.commande_id), 2) AS nb_moyen_lignes_par_commande
FROM lignes_commande lc;
```

**Réponse agent :**

## Nombre moyen de lignes de produits par commande

### Résultat

| Indicateur | Valeur |
|---|---|
| **Nombre moyen de lignes par commande** | **3,07** |

### Interprétation

En moyenne, chaque commande contient **un peu plus de 3 produits distincts** (3,07 lignes de commande).

### Contexte business

Cet indicateur, souvent appelé **"panier moyen en nombre de références"**, est utile pour :

- 📦 **Dimensionner la logistique** : prévoir le temps de préparation des colis
- 🛒 **Évaluer le cross-selling** : un chiffre plus élevé traduit une bonne capacité à inciter les clients à acheter plusieurs références
- 📊 **Benchmarker les performances commerciales** : si ce ratio augmente dans le temps, cela peut indiquer l'efficacité des recommandations produits ou des promotions groupées
- 🎯 **Fixer des objectifs** : par exemple, viser 4 lignes/commande via des stratégies de vente croisée

> **En résumé** : avec 3,07 lignes par commande, les clients achètent en moyenne **3 types de produits différents** à chaque passage de commande.

**Verdict juge :** Réponse correcte avec valeur 3,07 dans la plage attendue (1-5), bien expliquée.

---

### Q27 — Questions pièges / ambiguës

**Question :** Quel est le meilleur client ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    c.id AS client_id,
    c.nom AS client_nom,
    c.email,
    SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM clients c
JOIN commandes co ON co.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = co.id
WHERE co.statut = 'livré'
GROUP BY c.id, c.nom, c.email
ORDER BY ca_total DESC
LIMIT 1;
```

**Réponse agent :**

## 🏆 Meilleur Client

Le meilleur client, en termes de chiffre d'affaires généré sur les commandes **livrées**, est :

| Client ID | Nom | Email | CA Total |
|-----------|-----|-------|----------|
| 16 | **Stéphane-Marcel Guillon** | oetienne@example.org | **33 152,16 €** |

---

### 📊 Analyse Business

**Stéphane-Marcel Guillon** se distingue comme le client le plus précieux du portefeuille avec **33 152,16 €** de chiffre d'affaires cumulé sur l'ensemble de ses commandes livrées.

> **💡 Recommandations :**
> - Ce client mérite une attention particulière dans le cadre d'un programme de **fidélisation VIP**
> - Un suivi commercial personnalisé et des offres exclusives pourraient renforcer la relation et maximiser la rétention
> - Il serait pertinent d'analyser son **historique d'achats** (fréquence, catégories de produits) pour mieux anticiper ses besoins

**Verdict juge :** Interprétation claire (CA sur commandes livrées), nom du client et valeur fournis.

---

### Q28 — Questions pièges / ambiguës

**Question :** Combien avons-nous fait de ventes ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT COUNT(DISTINCT commandes.id) AS nombre_de_ventes
FROM commandes
WHERE commandes.statut = 'livré';
```

**Réponse agent :**

## Nombre de ventes réalisées

Nous avons réalisé **633 ventes** à ce jour, correspondant aux commandes ayant le statut **"livré"**.

> 💡 **Note business** : Ce chiffre représente uniquement les commandes effectivement livrées aux clients. Les commandes en cours de traitement, en transit ou annulées ne sont pas comptabilisées dans ce total, ce qui en fait un indicateur fiable des ventes **réellement conclues**.

**Verdict juge :** Interprétation claire (commandes livrées = 633), choix explicité et justifié business.

---

### Q29 — Questions pièges / ambiguës

**Question :** Quels clients sont inactifs ?

**Score :** 2/2

**SQL généré :**
```sql
SELECT
    c.id,
    c.nom,
    c.email,
    c.ville,
    c.date_inscription,
    MAX(cmd.date_commande) AS derniere_commande
FROM clients c
LEFT JOIN commandes cmd ON cmd.client_id = c.id AND cmd.statut != 'annulé'
GROUP BY c.id, c.nom, c.email, c.ville, c.date_inscription
HAVING derniere_commande IS NULL
    OR derniere_commande < DATE('2026-05-16', '-12 months')
ORDER BY derniere_commande ASC
LIMIT 20;
```

**Réponse agent :**

## Clients Inactifs

Un client est considéré comme **inactif** s'il n'a passé aucune commande valide, ou si sa dernière commande remonte à **plus de 12 mois** (avant le 16 mai 2025).

### Résultats (20 premiers clients, triés par ancienneté d'activité)

| ID | Nom | Email | Ville | Date d'inscription | Dernière commande |
|----|-----|-------|-------|--------------------|-------------------|
| 153 | Michel-Henri Philippe | gguillet@example.org | Montpellier | 2022-09-16 | ❌ Jamais commandé |
| 69 | Thérèse de la Delmas | jacquetdenise@example.net | Toulouse | 2022-08-26 | 2023-02-12 |
| 91 | Thibaut Seguin | merletherese@example.org | Nantes | 2024-04-17 | 2023-03-17 |
| 28 | Frédéric Andre-Maillot | pruvostfrancoise@example.org | Le Havre | 2022-05-03 | 2023-04-27 |
| 129 | Luc Buisson | descampselodie@example.com | Angers | 2022-07-25 | 2023-06-22 |
| 25 | René Gosselin | gilbertdelmas@example.com | Lyon | 2025-02-07 | 2023-08-10 |
| 112 | Arnaude Verdier | fernandeshenri@example.net | Lille | 2023-09-12 | 2023-08-26 |
| 197 | Patricia Maillard | olivieblanchet@example.org | Marseille | 2025-09-27 | 2023-10-21 |
| 60 | Luc Le Lopes | leleuroger@example.com | Montpellier | 2025-03-03 | 2023-11-12 |
| 38 | Frédérique Maréchal | gaillardalex@example.org | Bordeaux | 2023-12-06 | 2023-11-13 |
| 92 | Bernard Delorme de Langlois | tchauvin@example.org | Dijon | 2025-11-27 | 2023-11-27 |
| 100 | Patrick Lecomte | susanne45@example.com | Marseille | 2025-02-10 | 2023-12-11 |
| 156 | Gabriel Seguin Le Vasseur | lauredeschamps@example.net | Le Havre | 2025-11-02 | 2023-12-12 |
| 178 | Catherine du Gaudin | laetitiabertrand@example.net | Nîmes | 2023-01-18 | 2023-12-13 |
| 160 | Camille Le Gaillard | valerie74@example.net | Toulon | 2023-03-20 | 2023-12-31 |
| 137 | Claude Da Costa | carremonique@example.com | Toulon | 2025-09-03 | 2024-01-29 |
| 147 | Matthieu Brun | antoine05@example.org | Toulon | 2023-01-24 | 2024-03-07 |
| 77 | Raymond-Patrick Toussaint | robertbesnard@example.org | Toulouse | 2024-11-25 | 2024-03-07 |
| 200 | Daniel Le Charpentier | georges07@example.net | Toulon | 2025-07-19 | 2024-03-15 |
| 158 | Stéphane Marchal | ericcollet@example.com | Le Havre | 2022-01-04 | 2024-03

**Verdict juge :** Hypothèse explicite (>12 mois ou jamais commandé), liste de clients avec détails pertinents fournie.

---

### Q30 — Questions pièges / ambiguës

**Question :** Quel produit s'est le plus mal vendu ce trimestre ?

**Score :** 0/2

**SQL généré :**
```sql
SELECT p.id, p.nom, p.categorie,
       COALESCE(SUM(lc.quantite), 0) AS quantite_totale,
       COALESCE(SUM(lc.quantite * lc.prix_unitaire), 0) AS ca_total
FROM produits p
LEFT JOIN lignes_commande lc ON lc.produit_id = p.id
LEFT JOIN commandes c ON c.id = lc.commande_id
    AND c.statut != 'annulé'
    AND c.date_commande >= '2026-04-01'
    AND c.date_commande <= '2026-06-30'
GROUP BY p.id, p.nom, p.categorie
ORDER BY quantite_totale ASC
LIMIT 1;
```

**Réponse agent :**

## Produit le moins performant ce trimestre (Q2 2026)

### Résultat

| ID | Produit | Catégorie | Quantité vendue | Chiffre d'affaires |
|----|---------|-----------|-----------------|--------------------|
| 47 | Habiter Éle-47 | Électronique | 106 unités | 6 583,95 € |

### Analyse

Le produit **Habiter Éle-47** (catégorie Électronique) est celui qui s'est le **moins bien vendu** ce trimestre, avec seulement **106 unités écoulées** pour un chiffre d'affaires de **6 583,95 €**, soit un prix de vente moyen d'environ **62,11 € par unité**.

### Points d'attention business

- ⚠️ **Performance faible** : Avec 106 unités sur un trimestre entier (~35 unités/mois), ce produit mérite une attention particulière.
- 🔍 **Questions à se poser** :
  - S'agit-il d'un produit récent encore en phase de lancement ?
  - Y a-t-il un problème de visibilité, de prix ou de concurrence ?
  - Le stock est-il suffisant ou y a-t-il eu des ruptures ?
- 💡 **Actions possibles** : envisager une campagne promotionnelle, revoir le positionnement tarifaire, ou évaluer l'opportunité de déréférencer ce produit s'il mobilise des ressources logistiques sans retour suffisant.

> **Note** : Les commandes annulées ont été exclues de cette analyse, ce qui donne une vision fidèle des ventes effectives.

**Verdict juge :** Interprète 'ce trimestre' comme Q2 2026 (incorrect) et retourne des résultats sans signaler l'absence de données réelles.

---

## Analyse des résultats

### Score global : 51/60 (85%)

### Pattern d'erreur principal — biais "livré"
L'agent applique systématiquement un filtre `statut = 'livré'` même quand 
la question ne le demande pas (Q02, Q03, Q06, Q08). Cause : 4 points perdus 
sur un seul pattern.

### 3 améliorations prioritaires
1. Supprimer le filtre livré par défaut dans le system prompt
2. Ajouter une détection de date hors périmètre des données
3. Revoir le calcul du panier moyen (Q22)