# Site Kyro / LoderPlayz — déploiement

## Ce qu'il y a dans l'archive
- `dist/` : le site statique prêt à mettre en ligne (9 pages, sitemap, robots, 404).
- `build.py` : régénère `dist/` (une seule source pour tous les title/canonical/Schema).
- `check.py` : contrôle qualité (liens cassés, JSON-LD, doublons de title, sitemap).
- `src/assets/` : CSS et favicon.

## 1. Le domaine (à faire par toi, 10 min)
Le site est généré avec `https://loderplayz.com` comme domaine par défaut.
Si tu prends un autre domaine, régénère avec :

    KYRO_BASE_URL="https://ton-domaine.com" python3 build.py
    python3 check.py

Sans cette étape, les balises canonical et le sitemap pointeront vers le mauvais domaine.

## 2. Mise en ligne (gratuit)
Option la plus simple, Cloudflare Pages ou Netlify :
1. Crée un dépôt GitHub, pousse tout le projet.
2. Connecte le dépôt, dossier de publication = `dist`, pas de commande de build
   (ou `python3 build.py` si la plateforme le permet).
3. Branche le domaine dans l'interface.

GitHub Pages fonctionne aussi : pousse uniquement le contenu de `dist/` sur la branche
`gh-pages`. Ajoute un fichier `.nojekyll` vide à la racine.

## 3. Après la mise en ligne (obligatoire pour être indexé)
1. Google Search Console → ajouter la propriété du domaine → valider (DNS TXT).
2. Soumettre `https://ton-domaine.com/sitemap.xml`.
3. Demander l'indexation manuelle de `/`, `/kyro`, `/loderplayz`.
4. Bing Webmaster Tools : import direct depuis Search Console, 2 clics.
5. Test des résultats enrichis de Google sur `/kyro` : vérifier que l'entité Person
   est bien lue.

## 4. Playlist Shorts
La page `/shorts` n'affiche rien d'inventé. Pour la remplir :
1. Sur YouTube Studio, crée une playlist publique « Shorts » et ajoute-y tes Shorts.
2. Récupère son identifiant (`PL...` dans l'URL).
3. Régénère :

    KYRO_SHORTS_PLAYLIST="PLxxxxxxxx" KYRO_BASE_URL="https://ton-domaine.com" python3 build.py

## 5. Image Open Graph
`/assets/og.png` est référencé dans les balises mais n'existe pas encore.
Fais une image 1200×630 (ta bannière de chaîne recadrée suffit) et dépose-la dans
`src/assets/og.png`, puis régénère. Tant qu'elle manque, les partages Discord/X
n'afficheront pas de vignette.
