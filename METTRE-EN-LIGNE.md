# Mettre le site en ligne gratuitement — 15 minutes, aucun paiement

Le site est déjà généré pour l'adresse **https://loderplayz.github.io**.
Cette adresse est gratuite, en HTTPS, et Google l'indexe normalement.

---

## Étape 1 — Créer le compte GitHub (5 min)

1. Va sur https://github.com/signup
2. **Le nom d'utilisateur doit être exactement `loderplayz`** (tout en minuscules).
   C'est lui qui donne l'adresse `loderplayz.github.io`.
3. Si `loderplayz` est déjà pris, prends autre chose et dis-moi quoi :
   je régénère le site avec la bonne adresse (une seule variable change).

## Étape 2 — Créer le dépôt (2 min)

1. https://github.com/new
2. Repository name : **`loderplayz.github.io`** — ce nom exact, sinon le site
   sortira dans un sous-dossier et les URLs du sitemap seront fausses.
3. Public. Ne coche rien d'autre. → « Create repository ».

## Étape 3 — Envoyer les fichiers (3 min, sans ligne de commande)

Sur la page du dépôt vide : « uploading an existing file ».
Décompresse l'archive sur ton ordinateur, puis **glisse tout le contenu**
(les fichiers `build.py`, `check.py`, les dossiers `dist`, `src`, `.github`…)
dans la fenêtre. Puis « Commit changes ».

Attention : glisse le *contenu* du dossier, pas le dossier lui-même.

## Étape 4 — Activer Pages (1 min)

Dépôt → **Settings** → **Pages** (menu de gauche)
→ « Build and deployment », Source : **GitHub Actions**.

C'est tout. Le fichier `.github/workflows/deploy.yml` fait le reste : il regénère
le site, lance le contrôle qualité (et refuse de déployer si une erreur apparaît),
puis publie. Suis l'avancement dans l'onglet « Actions ».

Deux à trois minutes plus tard : **https://loderplayz.github.io**

À partir de là, chaque modification poussée se redéploie toute seule.

---

## Étape 5 — Se faire indexer (10 min, c'est l'étape qui compte)

Sans ça, le site existe mais Google ne le connaît pas.

1. https://search.google.com/search-console → « Ajouter une propriété »
   → **Préfixe d'URL** → `https://loderplayz.github.io/`
   → validation par **balise HTML** : Google te donne une ligne `<meta name="google-site-verification" ...>`.
   **Envoie-la moi**, je l'intègre proprement dans le générateur (une ligne dans `build.py`).
2. Une fois validé : « Sitemaps » → soumettre `sitemap.xml`.
3. « Inspection d'URL » → tester `https://loderplayz.github.io/` → « Demander l'indexation ».
   Répète pour `/loderplayz` et `/kyro`. C'est limité à quelques URLs par jour, ces trois-là suffisent.
4. https://www.bing.com/webmasters → « Importer depuis Search Console », 2 clics.

Compte une à deux semaines avant de voir les premières impressions. La requête
`loderplayz` devrait remonter en premier, c'est la moins disputée.

## Étape 6 — Relier YouTube au site (30 secondes, gros effet)

YouTube Studio → Personnalisation → Informations de base → Liens
→ ajouter « Site officiel » → `https://loderplayz.github.io`

C'est le signal qui dit à Google que la chaîne et le site sont la même entité.
Sans lui, les deux restent deux objets sans rapport.

---

## Plus tard : passer à un vrai domaine

Le jour où tu achètes `loderplayz.com`, rien n'est à refaire :

1. Change `KYRO_BASE_URL` dans `.github/workflows/deploy.yml`.
2. Settings → Pages → Custom domain → saisis le domaine.
3. Chez le registrar, un enregistrement CNAME vers `loderplayz.github.io`.
4. Dans Search Console, ajoute la nouvelle propriété.

L'ancienne adresse redirigera automatiquement, donc rien n'est perdu.
