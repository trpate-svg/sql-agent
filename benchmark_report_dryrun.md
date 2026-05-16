# Benchmark SQL Agent — 2026-05-16

*Mode dry-run — jugement Claude désactivé, scores non calculés.*

## Détail question par question

### Q01 — Top/flop simples

**Question :** Quel est le top 5 clients en chiffre d'affaires total ?

**SQL généré :**
```sql
SELECT c.id, c.nom, c.email, SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM clients c
JOIN commandes co ON co.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = co.id
WHERE co.statut = 'livré'
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

### 📊 Insights Business

- **Stéphane-Marcel Guillon** se détache nettement avec **33 152 €**, soit **+31%** au-dessus du 2ème client.
- Les **2ème et 3ème** clients (Vasseur et Auger-Delahaye) sont très proches avec seulement **175 € d'écart**, formant un duo quasi-équivalent.
- Ces 5 clients représentent un CA cumulé de **~124 096 €**, ce qui peut constituer un segment **VIP** à fidéliser en priorité.

> ⚠️ **Note** : Seules les commandes au statut **"livré"** ont été prises en compte. Les commandes en cours, annulées ou en attente sont exclues de ce calcul.

---

### Q02 — Top/flop simples

**Question :** Quel est le produit le plus vendu en quantité totale ?

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

Le produit le plus vendu (sur la base des commandes **livrées**) est :

| Produit | Quantité totale vendue |
|-------------|----------------------|
| **Chemin Vêt-39** | **154 unités** |

### 💡 Analyse business

**Chemin Vêt-39** se distingue comme le **best-seller** du catalogue avec **154 unités** écoulées sur les commandes effectivement livrées à ce jour.

Quelques points à considérer :
- Ce chiffre ne prend en compte **que les commandes au statut "livré"**, ce qui en fait un indicateur fiable des ventes réelles et non des simples intentions d'achat.
- Il serait pertinent d'**analyser les marges** associées à ce produit pour s'assurer qu'il est aussi rentable qu'il est populaire.
- Une attention particulière devrait être portée à la **gestion des stocks** de ce produit afin d'éviter toute rupture qui pourrait impacter le chiffre d'affaires.

---

### Q03 — Top/flop simples

**Question :** Quelle catégorie de produits génère le plus de chiffre d'affaires ?

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

## 📊 Catégorie la plus performante en chiffre d'affaires

| Catégorie | Chiffre d'affaires total |
|-----------|--------------------------|
| **Vêtements** | **380 651,66 €** |

### 💡 Analyse business

La catégorie **Vêtements** est clairement le **moteur principal de revenus**, générant **380 651,66 €** de chiffre d'affaires sur les commandes livrées.

Quelques points à noter :

- Ce chiffre est basé **uniquement sur les commandes au statut "livré"**, ce qui en fait un indicateur fiable du revenu **réellement encaissé**, excluant les commandes en cours ou annulées.
- Il serait pertinent de **comparer cette catégorie aux autres** pour mesurer son poids relatif dans le CA global et identifier d'éventuelles opportunités de croissance sur des catégories sous-performantes.

### 🔎 Recommandations
- **Approfondir l'analyse** : identifier les sous-catégories ou produits spécifiques qui tirent ce résultat vers le haut.
- **Sécuriser cette catégorie** : s'assurer de la disponibilité des stocks et de la satisfaction client sur ce segment stratégique.
- **Évaluer la rentabilité** : le CA élevé ne garantit pas une marge élevée — croiser avec les coûts serait une prochaine étape utile.

---

### Q04 — Top/flop simples

**Question :** Quels sont les 3 produits les moins vendus en quantité ?

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

Voici les produits ayant enregistré les plus faibles volumes de ventes (commandes hors annulations) :

| Rang | ID | Produit | Catégorie | Quantité vendue |
|------|----|---------|-----------|-----------------|
| 🥉 1er | 47 | Habiter Éle-47 | Électronique | 106 unités |
| 🥈 2ème | 35 | Vers Spo-35 | Sport | 111 unités |
| 🥇 3ème | 14 | Attacher Spo-14 | Sport | 124 unités |

---

### 💡 Analyse business

- **Habiter Éle-47** est le produit le moins performant avec seulement **106 unités** écoulées, ce qui peut indiquer un manque d'attractivité ou un problème de visibilité dans la catégorie Électronique.
- **La catégorie Sport est surreprésentée** avec 2 produits sur 3 dans ce classement, ce qui pourrait signaler une **faiblesse structurelle** de cette gamme ou une concurrence interne entre produits.
- L'écart entre le 1er et le 3ème est relativement faible (**18 unités**), suggérant des performances homogènes dans le bas du classement.

> ⚠️ **Actions recommandées** : envisager des actions marketing ciblées (promotions, mise en avant), ou analyser si ces produits sont candidats à un **déréférencement** pour optimiser le catalogue.

---

### Q05 — Top/flop simples

**Question :** Quel client a passé le plus grand nombre de commandes ?

**SQL généré :**
```sql
SELECT c.id, c.nom, c.email, COUNT(co.id) AS nombre_commandes
FROM clients c
JOIN commandes co ON co.client_id = c.id
GROUP BY c.id, c.nom, c.email
ORDER BY nombre_commandes DESC
LIMIT 1
```

**Réponse agent :**

## 🏆 Client le plus fidèle

Le client ayant passé le plus grand nombre de commandes est :

| ID | Nom | Email | Nombre de commandes |
|----|-----|-------|-------------------|
| 12 | Timothée-Roger Vasseur | zoe03@example.org | **15** |

### 📊 Analyse business

**Timothée-Roger Vasseur** se distingue comme le client le plus actif de la base avec **15 commandes** passées. C'est un profil à fort potentiel qui mérite une attention particulière :

- ✅ **Client fidèle** : un volume de commandes élevé traduit un engagement fort envers l'enseigne
- 🎯 **Action recommandée** : ce client est un candidat idéal pour un programme de **fidélité VIP** ou des offres personnalisées afin de maintenir et renforcer sa relation commerciale
- 📬 **Canal de contact disponible** : son adresse email permet d'engager des actions marketing ciblées

> 💡 Il serait également intéressant de croiser ce résultat avec le **chiffre d'affaires généré** par ce client, car un grand nombre de commandes ne signifie pas nécessairement la valeur la plus élevée.

---

### Q06 — Top/flop simples

**Question :** Quelle ville génère le plus de chiffre d'affaires total ?

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

**Angers** se positionne comme la ville la plus performante en termes de chiffre d'affaires, avec **130 216,45 €** de revenus générés sur les commandes livrées.

> **Note méthodologique :** Ce calcul prend uniquement en compte les commandes avec le statut **"livré"**, ce qui reflète le chiffre d'affaires réellement encaissé, excluant ainsi les commandes en cours ou annulées.

### 💡 Points d'attention business
- Il serait pertinent de **comparer ce résultat aux autres villes** pour évaluer l'écart de performance et identifier des opportunités de développement commercial dans d'autres zones géographiques.
- Une analyse complémentaire sur le **nombre de clients actifs à Angers** permettrait de déterminer si cette performance est due à un volume de clients élevé ou à une valeur moyenne de commande supérieure.

---

### Q07 — Top/flop simples

**Question :** Quel est le produit le plus cher du catalogue ?

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

| ID | Nom | Catégorie | Prix unitaire |
|----|-----|-----------|---------------|
| 2 | Descendre Bea-2 | Beauté | **492,01 €** |

### 💡 Insight Business

Le produit phare en termes de valeur unitaire appartient à la catégorie **Beauté**, avec un prix de **492,01 €**. Ce positionnement premium peut indiquer :
- Un produit **haut de gamme** ou de niche dans la gamme Beauté
- Un levier potentiel de **marge élevée** à surveiller dans les performances de vente
- Un candidat idéal pour des stratégies de **mise en avant commerciale** (vitrine, recommandations, bundles)

Il serait intéressant de croiser ce produit avec ses **volumes de vente** pour évaluer s'il contribue significativement au chiffre d'affaires global.

---

### Q08 — Top/flop simples

**Question :** Quels sont les 5 produits avec le CA total le plus élevé ?

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

Voici les 5 produits ayant généré le chiffre d'affaires le plus élevé, calculé **uniquement sur les commandes livrées** :

| Rang | Produit | Catégorie | CA Total |
|------|--------------------------|---------------|--------------|
| 🥇 1 | Amener Vêt-30 | Vêtements | 69 238,80 € |
| 🥈 2 | Descendre Bea-2 | Beauté | 57 457,70 € |
| 🥉 3 | Bon Mai-12 | Maison | 56 248,34 € |
| 4 | Claire Bea-28 | Beauté | 54 542,27 € |
| 5 | Or Éle-38 | Électronique | 53 301,96 € |

### 📊 Insights clés

- **Leader incontesté** : *Amener Vêt-30* (Vêtements) domine avec **69 238 €**, soit un écart de +20% par rapport au 2ème produit.
- **La Beauté bien représentée** : la catégorie place **2 produits** dans le top 5 (rangs 2 et 4), pour un cumul de ~112 000 €.
- **Écart resserré** : les positions 2 à 5 sont très proches (entre 53 300 € et 57 500 €), ce qui indique une **concurrence serrée** entre ces produits.
- **Diversité des catégories** : 4 catégories différentes sont représentées (Vêtements, Beauté, Maison, Électronique), signe d'un portefeuille de produits **bien équilibré**.

> ⚠️ *Ces chiffres excluent les commandes non livrées (annulées, en cours, etc.), et reflètent donc le CA réellement encaissé.*

---

### Q09 — Temporel / évolution

**Question :** Quel mois de 2024 a enregistré le plus grand nombre de commandes ?

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

## Analyse des commandes 2024

### Résultat

| Mois | Nombre de commandes |
|------|-------------------|
| Décembre 2024 | **70 commandes** |

### Interprétation

Le mois de **décembre 2024** est le mois ayant enregistré le **plus grand nombre de commandes** de l'année, avec **70 commandes** au total.

### Contexte business

Ce pic en décembre est cohérent avec les tendances commerciales habituelles, notamment :
- 🎄 **Les fêtes de fin d'année** (Noël, réveillon du Nouvel An) qui stimulent traditionnellement les achats
- Les **promotions saisonnières** et opérations commerciales de fin d'année
- Les **achats de cadeaux** et les commandes en anticipation des fêtes

> 💡 **Recommandation** : Il serait pertinent de comparer ce chiffre avec décembre des années précédentes pour évaluer la croissance, et d'analyser les autres mois de 2024 pour identifier d'éventuels autres pics (ex. : soldes de janvier, Saint-Valentin, Black Friday en novembre).

---

### Q10 — Temporel / évolution

**Question :** Quel est le chiffre d'affaires total par année ?

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

Voici l'évolution du chiffre d'affaires annuel sur les commandes **livrées** :

| Année | Chiffre d'affaires |
|-------|-------------------|
| 2023 | 414 436,77 € |
| 2024 | 467 580,77 € |
| 2025 | 496 693,18 € |

### 📊 Analyse

- **Tendance positive** : Le chiffre d'affaires est en **croissance continue** sur les 3 années observées.
- **2023 → 2024** : +53 144 € soit une hausse de **+12,8 %**
- **2024 → 2025** : +29 112 € soit une hausse de **+6,2 %**
- **Total cumulé** : **1 378 710,72 €** sur l'ensemble de la période

> ⚠️ **Note** : Ces chiffres n'incluent que les commandes avec le statut **"livré"**. Les commandes en cours, annulées ou en attente ne sont pas comptabilisées. Par ailleurs, les données 2025 peuvent être **partielles** selon la date d'extraction.

---

### Q11 — Temporel / évolution

**Question :** Compare le CA du premier trimestre 2024 avec celui du quatrième trimestre 2024.

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

| Trimestre | Chiffre d'Affaires | Évolution |
|-----------|-------------------|-----------|
| Q1 2024 | 72 045,71 € | — |
| Q4 2024 | 203 751,59 € | **+182,8 %** |

### 📊 Analyse

Le quatrième trimestre 2024 affiche un chiffre d'affaires de **203 751,59 €**, soit une progression de **+131 705,88 €** par rapport au premier trimestre (**72 045,71 €**), ce qui représente une croissance de près de **+183 %**.

### 💡 Points de contexte business

- **Q4 traditionnellement fort** : cette surperformance est cohérente avec les dynamiques saisonnières classiques (fêtes de fin d'année, Black Friday, soldes), qui boostent généralement les ventes en fin d'année.
- **Q1 structurellement plus faible** : le début d'année est souvent marqué par un ralentissement post-fêtes et une reprise progressive des achats.
- **Vigilance sur l'interprétation** : les résultats ne comptabilisent que les commandes au statut **"livré"**, ce qui peut sous-estimer le CA réel si certaines commandes sont encore en cours de traitement.

> ⚠️ Pour une analyse plus robuste, il serait utile de comparer ces trimestres avec les années précédentes (Q1 2023 vs Q1 2024 et Q4 2023 vs Q4 2024) afin de distinguer l'effet saisonnier d'une réelle tendance de croissance.

---

### Q12 — Temporel / évolution

**Question :** Quelle est l'évolution mensuelle du nombre de commandes en 2024 ?

**SQL généré :**
```sql
SELECT
    strftime('%m', date_commande) AS mois,
    COUNT(id) AS nombre_commandes
FROM commandes
WHERE strftime('%Y', date_commande) = '2024'
GROUP BY mois
ORDER BY mois;
```

**Réponse agent :**

## Évolution mensuelle des commandes en 2024

Voici le détail mois par mois du nombre de commandes enregistrées en 2024 :

| Mois | Nombre de commandes | Évolution vs mois précédent |
|------|--------------------|-----------------------------|
| Janvier | 13 | — |
| Février | 23 | +10 (+76,9%) |
| Mars | 17 | -6 (-26,1%) |
| Avril | 10 | -7 (-41,2%) |
| Mai | 21 | +11 (+110%) |
| Juin | 19 | -2 (-9,5%) |
| Juillet | 20 | +1 (+5,3%) |
| Août | 25 | +5 (+25%) |
| Septembre | 18 | -7 (-28%) |
| Octobre | 27 | +9 (+50%) |
| Novembre | 35 | +8 (+29,6%) |
| Décembre | 70 | +35 (+100%) |

**Total 2024 : 298 commandes**

---

### 📊 Points clés à retenir

- 📈 **Forte accélération en fin d'année** : le dernier trimestre (oct-nov-déc) concentre **132 commandes**, soit **44% du total annuel**.
- 🚀 **Décembre est le mois record** avec 70 commandes, soit **plus du double de novembre** (+100%), probablement porté par les achats de fin d'année (fêtes, promotions).
- ⚠️ **Avril est le point bas** de l'année avec seulement 10 commandes, signalant un possible creux saisonnier au printemps.
- 📉 **Le début d'année est timide** (janvier à avril), avec une moyenne de ~16 commandes/mois contre ~43 commandes/mois sur le dernier trimestre.

> **Recommandation** : Il serait pertinent d'analyser les causes de la faiblesse du mois d'avril et d'anticiper la montée en charge de fin d'année (stocks, logistique) au vu de la tendance haussière observée.

---

### Q13 — Temporel / évolution

**Question :** Quel trimestre de 2023 a enregistré le plus de commandes livrées ?

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

Le **4ème trimestre 2023** (octobre - décembre) est le trimestre ayant enregistré le **plus grand nombre de commandes livrées**, avec **84 livraisons**.

### Contexte business

Ce résultat est cohérent avec les tendances habituelles du commerce, car le T4 est généralement une période de forte activité commerciale, portée par :
- 🛍️ **Les fêtes de fin d'année** (Noël, réveillon)
- 🖤 **Le Black Friday / Cyber Monday** (novembre)
- 📦 Les achats anticipés de cadeaux

> **Point d'attention** : Ce chiffre reflète les commandes dont le **statut est "livré"** à la date de commande enregistrée. Il serait pertinent de croiser cette donnée avec le **chiffre d'affaires** généré sur ce trimestre pour mesurer l'impact financier réel de cette période de forte activité.

---

### Q14 — Temporel / évolution

**Question :** Montre le chiffre d'affaires par mois sur toutes les années pour visualiser la saisonnalité.

**SQL généré :**
```sql
SELECT
    strftime('%Y', c.date_commande) AS annee,
    strftime('%m', c.date_commande) AS mois,
    SUM(lc.quantite * lc.prix_unitaire) AS ca_total,
    COUNT(DISTINCT c.id) AS nb_commandes
FROM commandes c
JOIN lignes_commande lc ON lc.commande_id = c.id
WHERE c.statut = 'livré'
GROUP BY annee, mois
ORDER BY annee, mois
LIMIT 20;
```

**Réponse agent :**

## Chiffre d'affaires mensuel & Saisonnalité

### Données détaillées

| Année | Mois | CA Total (€) | Nb Commandes |
|-------|------|-------------:|-------------:|
| 2023 | Janvier | 22 912,62 € | 10 |
| 2023 | Février | 29 328,50 € | 12 |
| 2023 | **Mars** | **48 914,30 €** | 19 |
| 2023 | Avril | 6 789,37 € | 5 |
| 2023 | Mai | 16 505,85 € | 8 |
| 2023 | Juin | 33 831,92 € | 17 |
| 2023 | Juillet | 17 095,00 € | 10 |
| 2023 | Août | 36 919,73 € | 19 |
| 2023 | Septembre | 39 203,64 € | 14 |
| 2023 | Octobre | 23 865,87 € | 12 |
| 2023 | **Novembre** | **70 808,42 €** | 31 |
| 2023 | **Décembre** | **68 261,55 €** | 41 |
| 2024 | Janvier | 20 087,44 € | 9 |
| 2024 | Février | 36 561,21 € | 15 |
| 2024 | Mars | 15 397,06 € | 12 |
| 2024 | Avril | 17 695,55 € | 7 |
| 2024 | Mai | 27 519,07 € | 14 |
| 2024 | Juin | 38 901,65 € | 17 |
| 2024 | Juillet | 36 300,62 € | 16 |
| 2024 | **Août** | **48 468,35 €** | 19 |

---

### 📊 Analyse de la saisonnalité

#### 🔴 Points hauts identifiés
| Période | Signal | Explication probable |
|---------|--------|----------------------|
| **Nov–Déc 2023** | Pic majeur (+70K€ / +68K€) | Black Friday, fêtes de fin d'année, achats de Noël |
| **Mars 2023** | Pic de printemps (48K€) | Renouvellement post-hiver, budgets Q1 |
| **Août–Sept** | Rebond estival | Rentrée, achats de fin d'été |

#### 🟢 Points bas récurrents
| Période | Signal |
|---------|--------|
| **Avril 2023** | Creux marqué (6 789 € seulement — anomalie ?) |
| **Janvier** | Faible activité post-fêtes (~20-22K€) |
| **Mai 2023** | Creux de printemps (16 500 €) |

---

### 💡 Enseignements business

1. **La fin d'année est le moteur principal** : Novembre + Décembre 2023 représentent à eux seuls **~139 000 €**, soit environ **29% du CA annuel 2023** — un signal fort pour concentrer les efforts marketing et les stocks sur cette période.

2. **Avril 2023 est suspect** : avec seulement 6 789 € et 5 commandes, ce mois mérite investigation (problème opérationnel ? données manquantes ?).

3. **2024 montre une tendance haussière** : sur les mois comparables (Jan–Août), le CA semble globalement en progression, notamment en Juin (+15%) et Août (+31%) par rapport à 2023.

4. **Recommandation** : Planifier les campagnes promotionnelles dès **octobre** pour capitaliser sur le pic de fin d'année, et

---

### Q15 — Temporel / évolution

**Question :** Quel est le chiffre d'affaires total du mois de novembre 2024 ?

**SQL généré :**
```sql
SELECT SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM lignes_commande lc
JOIN commandes c ON lc.commande_id = c.id
WHERE c.statut = 'livré'
  AND strftime('%Y-%m', c.date_commande) = '2024-11';
```

**Réponse agent :**

## Chiffre d'affaires – Novembre 2024

Le chiffre d'affaires total réalisé au mois de **novembre 2024** s'élève à :

> # 💰 64 336,43 €

### Précisions méthodologiques
Ce montant est calculé sur la base des **commandes au statut "livré"** uniquement, ce qui reflète le chiffre d'affaires **effectivement encaissable**, en excluant les commandes en cours, annulées ou en attente.

### Points d'attention
- Ce chiffre **n'intègre pas les éventuelles remises globales**, retours ou avoirs qui pourraient minorer le CA net final.
- Il peut être utile de **comparer ce résultat** avec les mois précédents (septembre/octobre 2024) pour évaluer la tendance et l'impact des actions commerciales ou de la saisonnalité.

---

### Q16 — Filtres combinés

**Question :** Quels clients de Paris ont commandé des produits de la catégorie Électronique ?

**SQL généré :**
```sql
SELECT DISTINCT c.id, c.nom, c.email
FROM clients c
JOIN commandes co ON co.client_id = c.id
JOIN lignes_commande lc ON lc.commande_id = co.id
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

- **Segment identifié** : Ces 5 clients représentent votre cible *"Parisiens acheteurs d'Électronique"*, un profil potentiellement à forte valeur ajoutée.
- **Opportunités marketing** : Ce segment est idéal pour des campagnes ciblées (nouveautés électronique, offres de fidélité, upsell sur accessoires).
- **Volume modeste** : Seulement 5 clients correspondent à ces critères croisés, ce qui peut indiquer soit un marché de niche à Paris, soit un potentiel de croissance à explorer.

> 📌 *Il serait pertinent de croiser ces données avec le montant total dépensé par ces clients pour prioriser les actions commerciales.*

---

### Q17 — Filtres combinés

**Question :** Combien de commandes ont été annulées en 2024 ?

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

Ce chiffre mérite d'être mis en perspective pour en tirer des conclusions pertinentes :

- **Taux d'annulation** : il serait utile de le comparer au nombre total de commandes passées en 2024 pour calculer le pourcentage d'annulation.
- **Tendance** : une comparaison avec les années précédentes (2022, 2023) permettrait de déterminer si ce chiffre est en hausse, en baisse ou stable.
- **Causes** : identifier les raisons des annulations (rupture de stock, délais trop longs, erreurs de commande, etc.) aiderait à mettre en place des actions correctives.

> 💡 **Recommandation** : Si le taux d'annulation s'avère significatif, une analyse plus fine par période, par produit ou par client pourrait révéler des axes d'amélioration opérationnelle.

---

### Q18 — Filtres combinés

**Question :** Quel est le chiffre d'affaires total en comptant uniquement les commandes livrées ?

**SQL généré :**
```sql
SELECT SUM(lc.quantite * lc.prix_unitaire) AS ca_total
FROM lignes_commande lc
JOIN commandes c ON lc.commande_id = c.id
WHERE c.statut = 'livré';
```

**Réponse agent :**

## Chiffre d'affaires des commandes livrées

Le chiffre d'affaires généré par les **commandes effectivement livrées** s'élève à :

| Indicateur | Montant |
|---|---|
| **CA total (commandes livrées)** | **1 378 710,72 €** |

### 📊 Analyse business

Ce montant représente le **revenu réellement concrétisé**, c'est-à-dire les ventes pour lesquelles la livraison a bien été effectuée auprès des clients.

> ⚠️ **Point d'attention** : Ce chiffre exclut les commandes en cours de traitement, en attente ou annulées. Il est donc conseillé de le comparer au CA total (toutes commandes confondues) pour mesurer le **taux de concrétisation des ventes** et identifier d'éventuels points de blocage dans le processus de livraison.

---

### Q19 — Filtres combinés

**Question :** Quels produits de la catégorie Beauté ont un prix unitaire supérieur à 100 euros ?

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

## Produits Beauté avec un prix unitaire supérieur à 100 €

On recense **8 produits** dans la catégorie **Beauté** dont le prix unitaire dépasse 100 €. Voici le détail, classé du plus cher au moins cher :

| ID | Nom du produit | Catégorie | Prix unitaire (€) |
|----|----------------|-----------|------------------:|
| 2 | Descendre Bea-2 | Beauté | 492,01 € |
| 28 | Claire Bea-28 | Beauté | 442,65 € |
| 1 | Obtenir Bea-1 | Beauté | 353,25 € |
| 50 | Instant Bea-50 | Beauté | 220,11 € |
| 45 | But Bea-45 | Beauté | 202,84 € |
| 46 | Mien Bea-46 | Beauté | 168,92 € |
| 4 | Marchand Bea-4 | Beauté | 153,19 € |
| 9 | Repas Bea-9 | Beauté | 109,26 € |

### 📊 Quelques points clés

- **Prix maximum** : 492,01 € (*Descendre Bea-2*)
- **Prix minimum** (dans cette sélection) : 109,26 € (*Repas Bea-9*)
- **Prix moyen** de ces produits premium : ~268 €
- On observe une **forte disparité de prix** : les 3 premiers produits dépassent les 350 €, tandis que les 5 derniers se situent entre 109 € et 220 €.

> 💡 **Insight business** : Ces produits constituent le segment **haut de gamme** de la catégorie Beauté. Ils représentent une opportunité de **marge élevée**, mais nécessitent probablement une stratégie commerciale adaptée (positionnement premium, ciblage client spécifique).

---

### Q20 — Filtres combinés

**Question :** Quels clients de Lyon ont passé plus de 3 commandes ?

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

## Clients de Lyon ayant passé plus de 3 commandes

L'analyse révèle **5 clients lyonnais** particulièrement actifs, avec un minimum de 4 commandes chacun. Ces clients constituent un segment fidèle et à fort potentiel pour des actions de fidélisation ciblées.

| # | Nom | Email | Nombre de commandes |
|---|-----|-------|:-------------------:|
| 1 | François Perret Le Turpin | rpichon@example.org | 7 |
| 2 | Thomas Pereira | ruizsimone@example.com | 6 |
| 3 | Julie Bertrand du Regnier | hoareauedouard@example.net | 5 |
| 4 | Emmanuelle Torres | corinne74@example.org | 5 |
| 5 | Victoire-Clémence Cohen | vbarre@example.net | 4 |

### 📊 Points clés

- **François Perret Le Turpin** est le client le plus actif avec **7 commandes**, soit 40% de plus que le second.
- **2 clients** se situent à 5 commandes (Julie Bertrand du Regnier et Emmanuelle Torres).
- La moyenne pour ce groupe est de **5,4 commandes** par client.

### 💡 Recommandations business

- Ces 5 clients sont des **ambassadeurs potentiels** de votre marque à Lyon — envisager un programme de fidélité VIP ou des offres exclusives.
- Analyser le **panier moyen** de ces clients pour identifier s'ils sont également à forte valeur financière, pas seulement en volume.
- Ils pourraient être ciblés en priorité pour des **campagnes de réactivation** ou des **ventes croisées**.

---

### Q21 — Filtres combinés

**Question :** Quel est le panier moyen par ville pour les commandes livrées uniquement ?

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

## Panier moyen par ville – Commandes livrées

### Résultats

| Ville | Nb commandes livrées | Panier moyen |
|----------------|---------------------|--------------|
| Dijon | 29 | 2 552,92 € |
| Nantes | 34 | 2 549,37 € |
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
| Paris | 19 | 1 678,83 € |

---

### 📊 Enseignements clés

- 🥇 **Dijon et Nantes** dominent avec un panier moyen supérieur à **2 550 €**, malgré un volume de commandes modéré.
- 📦 **Angers, Montpellier et Bordeaux** combinent à la fois un **volume élevé** (50+ commandes) et un panier solide (> 2 000 €) — ce sont des marchés à fort potentiel.
- ⚠️ **Paris** affiche le panier moyen le plus bas (1 678 €) avec seulement 19 commandes livrées, ce qui est surprenant pour une capitale — cela mérite une investigation (mix produit différent ? clientèle spécifique ?).
- 🔍 **Le Havre et Lille** ont peu de commandes (8 et 11), ce qui rend leurs moyennes moins représentatives statistiquement.

### 💡 Recommandation
Concentrer les efforts commerciaux sur les villes à **fort volume ET panier élevé** (Angers, Montpellier, Bordeaux, Toulouse) tout en cherchant à comprendre pourquoi **Paris sous-performe** malgré son bassin de clientèle potentiel.

---

### Q22 — Agrégations complexes

**Question :** Quel est le panier moyen global par commande ?

**SQL généré :**
```sql
SELECT
    ROUND(SUM(lc.quantite * lc.prix_unitaire) / COUNT(DISTINCT lc.commande_id), 2) AS panier_moyen
FROM lignes_commande lc
JOIN commandes c ON lc.commande_id = c.id
WHERE c.statut != 'annulé';
```

**Réponse agent :**

## Panier Moyen Global par Commande

### Résultat

| Indicateur | Valeur |
|---|---|
| 🛒 Panier moyen par commande | **2 257,36 €** |

### Analyse business

Le panier moyen global s'établit à **2 257,36 €** par commande (hors commandes annulées).

**Points clés à retenir :**
- Ce chiffre représente la valeur moyenne dépensée par transaction, ce qui constitue un **KPI fondamental** pour évaluer la santé commerciale de l'entreprise.
- Les commandes annulées ont été **exclues du calcul** afin de refléter uniquement le chiffre d'affaires réellement généré ou en cours.

**Pistes d'analyse complémentaires :**
- 📊 **Segmenter** ce panier moyen par catégorie de clients, canal de vente ou période pour identifier des tendances
- 📈 **Suivre l'évolution** dans le temps pour mesurer l'efficacité des actions d'upselling/cross-selling
- 🎯 **Comparer** avec les benchmarks sectoriels pour situer la performance

---

### Q23 — Agrégations complexes

**Question :** Quelle est la valeur moyenne d'une ligne de commande par catégorie de produit ?

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

Voici la valeur moyenne générée par chaque ligne de commande, selon la catégorie de produit :

| Catégorie | Valeur moyenne d'une ligne |
|---------------|---------------------------|
| 🏅 Sport | 981,65 € |
| 👗 Vêtements | 757,09 € |
| 💄 Beauté | 745,93 € |
| 🏠 Maison | 705,85 € |
| 💻 Électronique | 638,12 € |

---

### 📊 Analyse business

**La catégorie Sport se démarque nettement** avec une valeur moyenne par ligne de **981,65 €**, soit **54 % de plus** que la catégorie Électronique, qui ferme le classement.

Quelques points clés à retenir :

- 🥇 **Sport** domine largement le classement, ce qui peut s'expliquer par des achats groupés (ex. : équipements en grande quantité) ou des produits à prix élevé (matériel sportif premium).
- 📦 **Vêtements et Beauté** sont proches (~750 €), suggérant des comportements d'achat similaires dans ces deux catégories.
- ⚡ **L'Électronique**, malgré sa réputation de produits coûteux, affiche la valeur la plus faible, ce qui peut indiquer des achats unitaires à prix modéré ou des remises fréquentes.

> **Recommandation** : Investir dans la mise en avant de la catégorie Sport (cross-selling, promotions ciblées) pourrait maximiser le panier moyen, tandis qu'une stratégie de montée en gamme sur l'Électronique mériterait d'être explorée.

---

### Q24 — Agrégations complexes

**Question :** Quel pourcentage des commandes sont annulées ?

**SQL généré :**
```sql
SELECT
    COUNT(CASE WHEN statut = 'annulé' THEN 1 END) AS nb_annulees,
    COUNT(*) AS nb_total,
    ROUND(COUNT(CASE WHEN statut = 'annulé' THEN 1 END) * 100.0 / COUNT(*), 2) AS pourcentage_annulees
FROM commandes;
```

**Réponse agent :**

## Taux d'annulation des commandes

Sur l'ensemble des commandes enregistrées, **83 commandes sur 909 sont annulées**, soit un taux d'annulation de :

> ### 🚫 9,13%

| Indicateur | Valeur |
|---|---|
| Commandes annulées | 83 |
| Total des commandes | 909 |
| **Taux d'annulation** | **9,13 %** |

---

### 📊 Analyse business

Un taux d'annulation de **9,13 %** est un signal à surveiller attentivement :

- **Benchmark e-commerce** : un taux sain se situe généralement **entre 2 % et 5 %**. À 9,13 %, ce taux est **au-dessus de la moyenne**, ce qui mérite investigation.
- **Pistes d'analyse** à explorer :
  - 🕐 **Délai de livraison** trop long → frustration client
  - 💳 **Problèmes de paiement** ou d'expérience d'achat
  - 📦 **Ruptures de stock** après commande passée
  - 🎯 **Segments clients ou produits** avec un taux d'annulation plus élevé

Il serait pertinent de **croiser ce taux par catégorie de produit, canal de vente ou période** pour identifier les leviers d'amélioration.

---

### Q25 — Agrégations complexes

**Question :** Combien de clients distincts ont passé plus d'une commande ?

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

D'après l'analyse des données de commandes (hors commandes annulées), **161 clients distincts** ont passé plus d'une commande sur la plateforme.

### Interprétation business

Ce chiffre est un indicateur clé de **fidélisation client** (repeat buyers). Ces 161 clients représentent la base de clients **récurrents**, c'est-à-dire ceux qui sont revenus effectuer au moins un second achat.

### Points à noter
- ✅ Les commandes **annulées ont été exclues** du calcul, ce qui donne une vision plus fidèle du comportement d'achat réel.
- 📊 Pour aller plus loin, il serait pertinent de **croiser ce chiffre avec le nombre total de clients actifs** afin de calculer le **taux de réachat** (ex : si la base compte 500 clients actifs, le taux serait de ~32%).
- 🎯 Ce segment de clients fidèles est généralement prioritaire pour des actions de **rétention et de programmes de fidélité**, car acquérir un nouveau client coûte en moyenne 5 à 7 fois plus cher que de fidéliser un client existant.

---

### Q26 — Agrégations complexes

**Question :** Quel est le nombre moyen de lignes de produits par commande ?

**SQL généré :**
```sql
SELECT CAST(COUNT(lc.id) AS FLOAT) / COUNT(DISTINCT lc.commande_id) AS nb_moyen_lignes_par_commande
FROM lignes_commande lc;
```

**Réponse agent :**

## Nombre moyen de lignes de produits par commande

### Résultat

| Indicateur | Valeur |
|---|---|
| Nombre moyen de lignes par commande | **3,07** |

### Analyse business

En moyenne, chaque commande contient **un peu plus de 3 produits distincts** (3,07 lignes exactement). Ce chiffre est un indicateur clé du comportement d'achat des clients :

- 📦 **Panier mixte** : Les clients ne se limitent pas à un seul produit, ce qui suggère une tendance à la commande groupée.
- 🎯 **Opportunités de cross-selling** : Avec ~3 lignes par commande, il existe une marge pour encourager les clients à ajouter davantage de produits (upsell/cross-sell) afin d'augmenter ce ratio.
- 📊 **Référence de performance** : Ce chiffre peut servir de **baseline** pour mesurer l'efficacité de campagnes promotionnelles (ex. : "Achetez X produits, obtenez une remise") ou de recommandations produits.

> 💡 Il serait intéressant de segmenter cet indicateur par **période**, **catégorie de client** ou **canal de vente** pour identifier des tendances plus fines.

---

### Q27 — Questions pièges / ambiguës

**Question :** Quel est le meilleur client ?

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

Le meilleur client, sur la base du **chiffre d'affaires généré par les commandes livrées**, est :

| Client ID | Nom | Email | CA Total |
|-----------|-----|-------|----------|
| 16 | **Stéphane-Marcel Guillon** | oetienne@example.org | **33 152,16 €** |

---

### 📊 Analyse Business

**Stéphane-Marcel Guillon** se distingue comme le client le plus valuable avec **33 152,16 €** de chiffre d'affaires, calculé sur l'ensemble de ses commandes effectivement **livrées**.

> ⚠️ **Note méthodologique** : Ce classement est basé uniquement sur les commandes au statut *"livré"*, ce qui reflète le **revenu réellement concrétisé**. Les commandes en cours, annulées ou en attente ne sont pas comptabilisées, ce qui en fait un indicateur fiable de la valeur réelle apportée par ce client.

**Recommandations :**
- 🎯 Envisager un programme de **fidélisation VIP** pour ce client
- 📞 Attribuer un **account manager dédié** pour maintenir la relation
- 🔍 Analyser ses habitudes d'achat pour identifier des opportunités de **cross-sell / upsell**

---

### Q28 — Questions pièges / ambiguës

**Question :** Combien avons-nous fait de ventes ?

**SQL généré :**
```sql
SELECT COUNT(DISTINCT commandes.id) AS nombre_de_ventes
FROM commandes
WHERE commandes.statut = 'livré';
```

**Réponse agent :**

## Nombre de ventes réalisées

Nous avons réalisé **633 ventes** à ce jour, correspondant aux commandes ayant le statut **"livré"**.

> 💡 **Note business** : Ce chiffre reflète uniquement les commandes effectivement livrées aux clients, ce qui constitue l'indicateur le plus fiable du volume de ventes concrétisées. Les commandes en cours de traitement ou annulées ne sont pas comptabilisées dans ce total.

---

### Q29 — Questions pièges / ambiguës

**Question :** Quels clients sont inactifs ?

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
ORDER BY derniere_commande ASC NULLS FIRST
LIMIT 20;
```

**Réponse agent :**

## Clients Inactifs

L'analyse identifie les clients **sans aucune commande valide** ou dont la **dernière commande remonte à plus de 12 mois** (avant le 16 mai 2025).

### Résultats (20 premiers sur potentiellement plus)

| ID | Nom | Email | Ville | Date d'inscription | Dernière commande |
|----|-----|-------|-------|-------------------|-------------------|
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
| 158 | Stéphane Marchal | ericcollet@example.com | Le Havre | 2022-01-04 | 2024-03-20 |

---

### 📊 Points clés

- **

---

### Q30 — Questions pièges / ambiguës

**Question :** Quel produit s'est le plus mal vendu ce trimestre ?

**SQL généré :**
```sql
SELECT p.id, p.nom, p.categorie,
       COALESCE(SUM(lc.quantite), 0) AS quantite_vendue,
       COALESCE(SUM(lc.quantite * lc.prix_unitaire), 0) AS ca_total
FROM produits p
LEFT JOIN lignes_commande lc ON lc.produit_id = p.id
LEFT JOIN commandes c ON c.id = lc.commande_id
    AND c.statut = 'livré'
    AND c.date_commande >= '2026-04-01'
    AND c.date_commande <= '2026-06-30'
GROUP BY p.id, p.nom, p.categorie
ORDER BY quantite_vendue ASC, ca_total ASC
LIMIT 1;
```

**Réponse agent :**

## Produit le moins vendu ce trimestre (Q2 2026)

### Résultat

| ID | Produit | Catégorie | Quantité vendue | Chiffre d'affaires |
|----|---------|-----------|-----------------|--------------------|
| 47 | Habiter Éle-47 | Électronique | 106 unités | 6 583,95 € |

### Analyse

Le produit **Habiter Éle-47** (catégorie Électronique) est celui qui s'est le **moins bien vendu** ce trimestre avec seulement **106 unités écoulées**, générant un chiffre d'affaires de **6 583,95 €**, soit un prix moyen unitaire d'environ **62,11 €**.

### Points d'attention business

- 📉 **106 unités** représente le plancher des ventes sur la période — il convient de comparer ce chiffre avec les trimestres précédents pour déterminer s'il s'agit d'une **tendance structurelle** ou d'un **creux ponctuel**.
- 🔍 Plusieurs hypothèses méritent d'être explorées :
  - **Problème de visibilité** (référencement, merchandising)
  - **Prix peu compétitif** par rapport à des produits similaires
  - **Fin de cycle de vie** du produit
  - **Ruptures de stock** ponctuelles ayant freiné les ventes
- ⚠️ Il serait également utile de vérifier si ce produit affiche des **marges faibles**, auquel cas une révision de l'assortiment pourrait être envisagée.

> 💡 **Recommandation** : Croiser ces données avec les retours clients et les niveaux de stock pour décider d'une action corrective (promotion, déréférencement, ou relance marketing).

---
