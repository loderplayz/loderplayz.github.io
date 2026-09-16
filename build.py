#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur statique du site officiel Kyro / LoderPlayz.
Aucune donnée non vérifiée n'est écrite dans les pages.
Usage: python3 build.py   ->  ./dist
"""
import json, os, re, shutil, datetime, sys

# ---------------------------------------------------------------- CONFIG
# !! À CHANGER par le domaine réellement acheté avant déploiement.
BASE = os.environ.get("KYRO_BASE_URL", "https://loderplayz.com").rstrip("/")

CHANNEL_ID   = "UC3iBa-hqBpZbPzFg6WBtsnQ"          # vérifié
UPLOADS_PL   = "UU" + CHANNEL_ID[2:]                # playlist "uploads" = UC->UU
SHORTS_PL    = os.environ.get("KYRO_SHORTS_PLAYLIST", "")  # à créer manuellement sur YouTube
HANDLE       = "@LoderPlayz"
CHANNEL_URL  = "https://www.youtube.com/" + HANDLE
DISCORD_URL  = "https://discord.gg/GH9ekm5JC"       # tiré de la bio du canal
BUILD_DATE   = datetime.date.today().isoformat()

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

# ---------------------------------------------------------------- SCHEMA
PERSON_ID  = f"{BASE}/kyro#person"
CHANNEL_ID_URI = f"{BASE}/loderplayz#channel"
SITE_ID    = f"{BASE}/#website"

SAME_AS = [CHANNEL_URL, f"https://www.youtube.com/channel/{CHANNEL_ID}"]

def schema_person():
    return {
        "@type": "Person",
        "@id": PERSON_ID,
        "name": "Kyro",
        "alternateName": ["LoderPlayz", HANDLE],
        "url": f"{BASE}/kyro",
        "jobTitle": "Créateur de contenu vidéo",
        "description": ("Kyro, connu en ligne sous le pseudonyme LoderPlayz "
                        f"({HANDLE}), est un créateur YouTube de contenus Minecraft et Roblox."),
        "sameAs": SAME_AS,
        "knowsAbout": ["Minecraft", "Roblox", "Montage vidéo de jeu", "YouTube Shorts"],
        "mainEntityOfPage": {"@id": f"{BASE}/kyro#webpage"},
        "subjectOf": {"@id": CHANNEL_ID_URI},
    }

def schema_channel():
    return {
        "@type": "ProfilePage",
        "@id": CHANNEL_ID_URI,
        "name": f"LoderPlayz ({HANDLE})",
        "url": CHANNEL_URL,
        "about": {"@id": PERSON_ID},
        "mainEntity": {"@id": PERSON_ID},
    }

def schema_website():
    return {
        "@type": "WebSite",
        "@id": SITE_ID,
        "url": BASE + "/",
        "name": "Kyro – LoderPlayz",
        "inLanguage": "fr",
        "publisher": {"@id": PERSON_ID},
        "about": {"@id": PERSON_ID},
    }

def breadcrumbs(path, title):
    items = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"}]
    if path:
        items.append({"@type": "ListItem", "position": 2, "name": title,
                      "item": f"{BASE}/{path}"})
    return {"@type": "BreadcrumbList", "itemListElement": items}

# ---------------------------------------------------------------- LAYOUT
NAV = [
    ("", "Accueil"),
    ("kyro", "Kyro"),
    ("loderplayz", "LoderPlayz"),
    ("videos", "Vidéos"),
    ("shorts", "Shorts"),
    ("guides", "Guides"),
    ("about", "À propos"),
    ("contact", "Contact"),
]

def url_for(path):
    return "/" if path == "" else f"/{path}"

def render(page):
    path, title, desc, body = page["path"], page["title"], page["desc"], page["body"]
    canonical = BASE + url_for(path)
    graph = page.get("graph", [])
    graph = graph + [breadcrumbs(path, page.get("nav_title", title))]
    jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                        ensure_ascii=False, indent=1)
    nav = "\n".join(
        f'        <li><a href="{url_for(p)}"{" aria-current=\"page\"" if p == path else ""}>{t}</a></li>'
        for p, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="{page.get('og_type','website')}">
<meta property="og:site_name" content="Kyro – LoderPlayz">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{BASE}/assets/og.png">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=Inter+Tight:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{jsonld}
</script>
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<header class="top">
  <a class="mark" href="/"><span>KY</span><span>RO</span></a>
  <nav aria-label="Navigation principale">
    <ul>
{nav}
    </ul>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <p><strong>Kyro</strong> — aussi connu sous <strong>LoderPlayz</strong> ({HANDLE}).
     Chaîne&nbsp;: <a href="{CHANNEL_URL}" rel="me">youtube.com/{HANDLE}</a> ·
     Communauté&nbsp;: <a href="{DISCORD_URL}" rel="nofollow noopener">Discord</a></p>
  <p class="fine">Site officiel. Dernière mise à jour&nbsp;: {BUILD_DATE}.
     Minecraft et Roblox sont des marques de leurs détenteurs respectifs&nbsp;;
     ce site n'est ni affilié ni approuvé par eux.</p>
</footer>
</body>
</html>
"""

# ---------------------------------------------------------------- PAGES
def pages():
    P = []

    P.append(dict(path="", title="Kyro (LoderPlayz) — site officiel de la chaîne YouTube",
        desc=f"Site officiel de Kyro, alias LoderPlayz ({HANDLE}) : vidéos et Shorts "
             "Minecraft et Roblox, guides, Discord et contact.",
        graph=[schema_website(), schema_person(), schema_channel()],
        body=f"""
<section class="hero">
  <p class="kicker">Site officiel</p>
  <h1>Kyro<span class="alias">alias LoderPlayz</span></h1>
  <p class="lede">Je fais des vidéos et des Shorts <strong>Minecraft</strong> et
  <strong>Roblox</strong> sur la chaîne YouTube <a href="{CHANNEL_URL}" rel="me">{HANDLE}</a>.
  Cette page rassemble tout&nbsp;: les dernières vidéos, les Shorts, le Discord et le contact.</p>
  <p class="cta-row">
    <a class="btn" href="{CHANNEL_URL}" rel="me">Voir la chaîne YouTube</a>
    <a class="btn ghost" href="/videos">Dernières vidéos</a>
  </p>
</section>

<section class="band">
  <h2>Un seul créateur, trois noms</h2>
  <div class="grid3">
    <article><h3><a href="/kyro">Kyro</a></h3>
      <p>Le nom utilisé par la chaîne et la communauté.</p></article>
    <article><h3><a href="/loderplayz">LoderPlayz</a></h3>
      <p>Le pseudo historique, celui du handle YouTube.</p></article>
    <article><h3><a href="{CHANNEL_URL}" rel="me">{HANDLE}</a></h3>
      <p>Le handle officiel. Tout autre compte n'est pas moi.</p></article>
  </div>
</section>

<section class="band">
  <h2>Les dernières vidéos</h2>
  <p>La liste se met à jour automatiquement depuis YouTube.</p>
  {embed(UPLOADS_PL, "Dernières vidéos de LoderPlayz")}
  <p><a href="/videos">Page vidéos</a> · <a href="/shorts">Page Shorts</a></p>
</section>

<section class="band">
  <h2>Guides</h2>
  <p>Des pages écrites pour répondre à des questions posées en commentaire,
     pas pour remplir le site.</p>
  <ul class="links">
    <li><a href="/guides/enregistrer-minecraft-roblox">Enregistrer Minecraft et Roblox proprement sans faire ramer son PC</a></li>
  </ul>
</section>
"""))

    P.append(dict(path="kyro", title="Qui est Kyro ? Le créateur derrière LoderPlayz",
        nav_title="Kyro",
        desc="Kyro est le nom du créateur de la chaîne YouTube LoderPlayz "
             f"({HANDLE}), spécialisée en Minecraft et Roblox.",
        og_type="profile",
        graph=[{**schema_person(), "mainEntityOfPage": {"@id": f"{BASE}/kyro#webpage"}},
               {"@type": "WebPage", "@id": f"{BASE}/kyro#webpage",
                "url": f"{BASE}/kyro", "name": "Qui est Kyro ?",
                "isPartOf": {"@id": SITE_ID}, "about": {"@id": PERSON_ID}}],
        body=f"""
<article class="prose">
<h1>Qui est Kyro&nbsp;?</h1>
<p><strong>Kyro</strong> est le nom du créateur de la chaîne YouTube
<a href="{CHANNEL_URL}" rel="me">{HANDLE}</a>, également connu sous le pseudonyme
<a href="/loderplayz">LoderPlayz</a>. La chaîne publie des vidéos et des Shorts
autour de deux jeux&nbsp;: <strong>Minecraft</strong> et <strong>Roblox</strong>,
avec une part de montage et d'édits.</p>

<h2>À ne pas confondre</h2>
<p>«&nbsp;Kyro&nbsp;» est un nom porté par beaucoup de comptes&nbsp;: d'autres chaînes YouTube,
des comptes TikTok, des objets Roblox. Le seul identifiant qui ne se confond avec rien
est le handle YouTube <strong>{HANDLE}</strong> et l'identifiant de chaîne
<code>{CHANNEL_ID}</code>.</p>

<h2>Comptes officiels</h2>
<ul class="links">
  <li>YouTube&nbsp;: <a href="{CHANNEL_URL}" rel="me">youtube.com/{HANDLE}</a></li>
  <li>Discord&nbsp;: <a href="{DISCORD_URL}" rel="nofollow noopener">serveur de la communauté</a></li>
</ul>
<p>Cette liste est la référence. Elle est mise à jour ici en premier&nbsp;; si un compte
n'y figure pas, il n'est pas à moi.</p>

<h2>Le contenu</h2>
<p>Deux formats cohabitent&nbsp;: des <a href="/videos">vidéos longues</a> de gameplay et
des <a href="/shorts">Shorts</a> courts et rythmés. <a href="/about">En savoir plus
sur la chaîne</a>.</p>
</article>
"""))

    P.append(dict(path="loderplayz", title=f"LoderPlayz ({HANDLE}) — la chaîne de Kyro",
        nav_title="LoderPlayz",
        desc=f"LoderPlayz {HANDLE} est la chaîne YouTube de Kyro : Minecraft, Roblox, "
             "Shorts et édits. Lien officiel et présentation.",
        graph=[schema_channel(), schema_person(),
               {"@type": "WebPage", "@id": f"{BASE}/loderplayz#webpage",
                "url": f"{BASE}/loderplayz", "name": "LoderPlayz",
                "isPartOf": {"@id": SITE_ID}, "about": {"@id": PERSON_ID}}],
        body=f"""
<article class="prose">
<h1>LoderPlayz</h1>
<p><strong>LoderPlayz</strong> est le pseudonyme et le handle YouTube de
<a href="/kyro">Kyro</a>. Le nom s'écrit en un seul mot, sans espace ni tiret&nbsp;;
le handle exact est <strong>{HANDLE}</strong>.</p>

<h2>Orthographes proches</h2>
<p>Plusieurs chaînes portent un nom voisin — LorDPlayZ, Lendemplayz, LDPlayz —
et n'ont aucun lien avec celle-ci. La chaîne dont parle ce site est celle dont
l'identifiant est <code>{CHANNEL_ID}</code>.</p>

<h2>Voir la chaîne</h2>
{embed(UPLOADS_PL, "Vidéos de la chaîne LoderPlayz")}
<p><a class="btn" href="{CHANNEL_URL}" rel="me">S'abonner sur YouTube</a></p>
</article>
"""))

    P.append(dict(path="videos", title="Vidéos Minecraft et Roblox de Kyro (LoderPlayz)",
        nav_title="Vidéos",
        desc="Toutes les vidéos de la chaîne LoderPlayz, mises à jour automatiquement : "
             "gameplay Minecraft, Roblox et montages.",
        graph=[{"@type": "CollectionPage", "@id": f"{BASE}/videos#webpage",
                "url": f"{BASE}/videos", "name": "Vidéos",
                "isPartOf": {"@id": SITE_ID}, "about": {"@id": PERSON_ID}}],
        body=f"""
<article class="prose">
<h1>Vidéos</h1>
<p>Les vidéos les plus récentes de <a href="/loderplayz">LoderPlayz</a>, dans l'ordre
de publication. La liste vient directement de YouTube&nbsp;: elle se met à jour sans
intervention.</p>
{embed(UPLOADS_PL, "Toutes les vidéos de LoderPlayz")}
<h2>Ce qu'on y trouve</h2>
<p>Du gameplay <strong>Minecraft</strong>, du <strong>Roblox</strong> et des montages.
Pour les formats courts, voir la <a href="/shorts">page Shorts</a>.</p>
<h2>Proposer une idée</h2>
<p>Les idées de vidéos passent par le <a href="{DISCORD_URL}" rel="nofollow noopener">Discord</a>
ou par la <a href="/contact">page contact</a>.</p>
</article>
"""))

    shorts_block = (embed(SHORTS_PL, "Shorts de LoderPlayz") if SHORTS_PL else
        """<p class="note">Aucune playlist Shorts n'est encore publiée sur la chaîne.
Dès qu'une playlist «&nbsp;Shorts&nbsp;» existe, son identifiant est à renseigner dans
la configuration du site (<code>KYRO_SHORTS_PLAYLIST</code>) et la liste apparaît ici
automatiquement. Aucun contenu inventé n'est affiché en attendant.</p>""")
    P.append(dict(path="shorts", title="Shorts de Kyro (LoderPlayz) — Minecraft et Roblox",
        nav_title="Shorts",
        desc="Les Shorts YouTube de LoderPlayz : formats courts Minecraft et Roblox, "
             "édits et moments de gameplay.",
        graph=[{"@type": "CollectionPage", "@id": f"{BASE}/shorts#webpage",
                "url": f"{BASE}/shorts", "name": "Shorts",
                "isPartOf": {"@id": SITE_ID}, "about": {"@id": PERSON_ID}}],
        body=f"""
<article class="prose">
<h1>Shorts</h1>
<p>Les formats courts de <a href="/loderplayz">LoderPlayz</a>&nbsp;: séquences de gameplay
Minecraft et Roblox, édits, moments marquants.</p>
{shorts_block}
<p><a href="{CHANNEL_URL}" rel="me">Voir les Shorts sur la chaîne</a> ·
   <a href="/videos">Vidéos longues</a></p>
</article>
"""))

    P.append(dict(path="guides", title="Guides Minecraft et Roblox — Kyro (LoderPlayz)",
        nav_title="Guides",
        desc="Guides pratiques écrits par Kyro (LoderPlayz) à partir des questions "
             "posées par la communauté.",
        graph=[{"@type": "CollectionPage", "@id": f"{BASE}/guides#webpage",
                "url": f"{BASE}/guides", "name": "Guides",
                "isPartOf": {"@id": SITE_ID}, "author": {"@id": PERSON_ID}}],
        body="""
<article class="prose">
<h1>Guides</h1>
<p>Une page n'est ajoutée ici que si une question revient vraiment en commentaire ou
sur le Discord. Pas de remplissage.</p>
<ul class="links">
  <li><a href="/guides/enregistrer-minecraft-roblox">Enregistrer Minecraft et Roblox
      proprement sans faire ramer son PC</a></li>
</ul>
</article>
"""))

    P.append(dict(path="guides/enregistrer-minecraft-roblox",
        title="Enregistrer Minecraft et Roblox sans faire ramer son PC",
        nav_title="Enregistrer sans lag",
        desc="Réglages d'enregistrement pour Minecraft et Roblox quand le PC est "
             "limité : encodeur, résolution, débit, audio et erreurs fréquentes.",
        og_type="article",
        graph=[{"@type": "Article", "@id": f"{BASE}/guides/enregistrer-minecraft-roblox#article",
                "headline": "Enregistrer Minecraft et Roblox sans faire ramer son PC",
                "author": {"@id": PERSON_ID}, "publisher": {"@id": PERSON_ID},
                "inLanguage": "fr", "dateModified": BUILD_DATE,
                "mainEntityOfPage": f"{BASE}/guides/enregistrer-minecraft-roblox",
                "about": [{"@type": "VideoGame", "name": "Minecraft"},
                          {"@type": "VideoGame", "name": "Roblox"}]}],
        body="""
<article class="prose">
<h1>Enregistrer Minecraft et Roblox sans faire ramer son PC</h1>
<p>C'est la question qui revient le plus souvent en commentaire. Le problème n'est
presque jamais le logiciel de capture&nbsp;: c'est le fait de demander au processeur
de faire tourner le jeu <em>et</em> de compresser la vidéo en même temps.</p>

<h2>Utiliser l'encodeur de la carte graphique</h2>
<p>Dans OBS, l'encodeur par défaut (x264) travaille sur le processeur, celui qui fait
déjà tourner Minecraft. Si la machine a un GPU NVIDIA, AMD récent ou un Intel avec
Quick Sync, l'encodeur matériel correspondant (NVENC, AMF, QSV) libère presque
entièrement le processeur. C'est le seul réglage qui change tout le reste&nbsp;;
à faire avant de toucher à quoi que ce soit d'autre.</p>

<h2>Choisir la résolution avant le débit</h2>
<p>Enregistrer en 1080p à 60&nbsp;images par seconde demande beaucoup plus de travail
qu'en 1080p à 30. Sur une machine juste, mieux vaut du 1080p30 net que du 1080p60 qui
saccade&nbsp;: une vidéo qui saute est plus désagréable à regarder qu'une vidéo à 30&nbsp;fps.
Pour les Shorts, l'image finale est verticale&nbsp;: enregistrer en 1080p horizontal et
recadrer au montage laisse plus de marge que de capturer directement en vertical.</p>

<h2>Ne pas confondre débit d'enregistrement et débit de live</h2>
<p>Pour un fichier gardé en local, il n'y a pas de limite d'upload&nbsp;: un débit
généreux, ou un mode à qualité constante, évite le flou dans les scènes qui bougent
beaucoup — typiquement une course en Roblox ou une explosion en Minecraft. Compresser
fort n'a d'intérêt qu'en direct.</p>

<h2>Séparer les pistes audio</h2>
<p>Enregistrer le jeu, le micro et la musique sur des pistes séparées prend le même
temps sur le moment et sauve le montage&nbsp;: on peut baisser la musique sous une
réplique sans toucher au reste. Avec une seule piste, c'est impossible.</p>

<h2>Les erreurs qui coûtent le plus</h2>
<ul>
  <li>Capturer l'écran entier au lieu de la fenêtre du jeu&nbsp;: plus lourd, et on
      enregistre ses notifications.</li>
  <li>Écrire le fichier sur le même disque que le jeu quand il s'agit d'un disque dur
      mécanique&nbsp;: des images perdues en pleine partie.</li>
  <li>Laisser le navigateur et une dizaine d'onglets ouverts pendant l'enregistrement.</li>
  <li>Découvrir après trois heures de jeu que le micro n'était pas branché. Tester
      trente secondes et réécouter, chaque fois.</li>
</ul>

<h2>Vérifier avant de lancer la vraie session</h2>
<p>Un test de deux minutes, puis on regarde le fichier&nbsp;: image fluide, son présent
sur les deux pistes, pas d'images perdues dans les statistiques d'OBS. Si quelque chose
cloche, c'est maintenant qu'on le corrige, pas après.</p>

<p>Une question sur un réglage précis&nbsp;? Le
<a href="/contact">contact</a> et le Discord sont là pour ça.</p>
</article>
"""))

    P.append(dict(path="about", title="À propos de la chaîne LoderPlayz — Kyro",
        nav_title="À propos",
        desc="La chaîne LoderPlayz de Kyro : ce qu'on y trouve, les formats publiés "
             "et comment suivre les nouveautés.",
        graph=[{"@type": "AboutPage", "@id": f"{BASE}/about#webpage",
                "url": f"{BASE}/about", "name": "À propos",
                "isPartOf": {"@id": SITE_ID}, "about": {"@id": PERSON_ID}}],
        body=f"""
<article class="prose">
<h1>À propos</h1>
<p>Je m'appelle <a href="/kyro">Kyro</a>, je publie sous le pseudo
<a href="/loderplayz">LoderPlayz</a>. La chaîne a commencé sur Minecraft, puis Roblox
s'est ajouté, avec des édits et des formats courts.</p>

<h2>Les formats</h2>
<p>Des <a href="/videos">vidéos longues</a> pour le gameplay et les séries,
des <a href="/shorts">Shorts</a> pour les moments courts.</p>

<h2>Où suivre</h2>
<ul class="links">
  <li><a href="{CHANNEL_URL}" rel="me">La chaîne YouTube {HANDLE}</a></li>
  <li><a href="{DISCORD_URL}" rel="nofollow noopener">Le Discord</a> — annonces et idées de vidéos</li>
</ul>

<h2>Objectif affiché</h2>
<p>Le cap annoncé sur la chaîne est 1&nbsp;000 abonnés. Il est public, donc autant
l'écrire ici aussi.</p>
</article>
"""))

    P.append(dict(path="contact", title="Contact — Kyro (LoderPlayz)",
        nav_title="Contact",
        desc="Contacter Kyro (LoderPlayz) : collaborations, propositions de vidéos "
             "et questions, via Discord ou YouTube.",
        graph=[{"@type": "ContactPage", "@id": f"{BASE}/contact#webpage",
                "url": f"{BASE}/contact", "name": "Contact",
                "isPartOf": {"@id": SITE_ID}, "about": {"@id": PERSON_ID}}],
        body=f"""
<article class="prose">
<h1>Contact</h1>
<p>Le plus rapide reste le Discord&nbsp;: j'y passe tous les jours.</p>
<ul class="links">
  <li><a href="{DISCORD_URL}" rel="nofollow noopener">Serveur Discord</a> — questions,
      idées, collaborations entre créateurs</li>
  <li><a href="{CHANNEL_URL}" rel="me">Commentaires YouTube</a> — sous les vidéos</li>
</ul>
<h2>Collaborations</h2>
<p>Les collabs avec d'autres créateurs Minecraft ou Roblox sont bienvenues. Un message
sur le Discord avec le lien de votre chaîne et l'idée en deux lignes suffit.</p>
<p class="note">Une adresse e-mail publique sera ajoutée ici lorsqu'elle existera.
Rien n'est affiché tant que ce n'est pas réel.</p>
</article>
"""))
    return P

def embed(playlist_id, label):
    src = f"https://www.youtube-nocookie.com/embed/videoseries?list={playlist_id}"
    return (f'<div class="embed"><iframe src="{src}" title="{label}" loading="lazy" '
            'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen '
            'allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture">'
            '</iframe></div>')

# ---------------------------------------------------------------- BUILD
def write(rel, text):
    dst = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    P = pages()
    for p in P:
        rel = "index.html" if p["path"] == "" else f'{p["path"]}/index.html'
        write(rel, render(p))

    # assets
    src_assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "assets")
    if os.path.isdir(src_assets):
        shutil.copytree(src_assets, os.path.join(OUT, "assets"))

    # 404
    write("404.html", render(dict(
        path="404", title="Page introuvable — Kyro (LoderPlayz)",
        desc="Cette page n'existe pas.", body="""
<article class="prose"><h1>Cette page n'existe pas</h1>
<p>Le lien est peut-être ancien. Les <a href="/videos">vidéos</a>,
les <a href="/shorts">Shorts</a> et la <a href="/">page d'accueil</a> fonctionnent.</p>
</article>""")).replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
                        '<meta name="robots" content="noindex, follow">'))

    # sitemap
    prio = {"": "1.0", "kyro": "0.9", "loderplayz": "0.9", "videos": "0.8",
            "shorts": "0.8", "guides": "0.6", "about": "0.5", "contact": "0.4"}
    urls = "\n".join(
        f"  <url><loc>{BASE}{url_for(p['path'])}</loc>"
        f"<lastmod>{BUILD_DATE}</lastmod>"
        f"<priority>{prio.get(p['path'],'0.6')}</priority></url>" for p in P)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          f"{urls}\n</urlset>\n")

    write("robots.txt", f"""User-agent: *
Allow: /

# Moteurs et assistants IA : accès explicitement autorisé
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {BASE}/sitemap.xml
""")

    n = len(P)
    print(f"[ok] {n} pages + 404 + sitemap.xml + robots.txt -> {OUT}")
    print(f"[ok] base URL = {BASE}")
    if not SHORTS_PL:
        print("[warn] KYRO_SHORTS_PLAYLIST vide : la page /shorts affiche une note honnête.")

if __name__ == "__main__":
    main()
