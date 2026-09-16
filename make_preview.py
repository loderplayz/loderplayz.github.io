#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble dist/ en un aperçu mono-page auto-suffisant (CSS inline)."""
import os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
OUT = "/mnt/user-data/outputs/kyro-loderplayz-apercu.html"

PAGES = [("", "Accueil"), ("kyro", "Kyro"), ("loderplayz", "LoderPlayz"),
         ("videos", "Vidéos"), ("shorts", "Shorts"), ("guides", "Guides"),
         ("guides/enregistrer-minecraft-roblox", "Guide : enregistrer sans lag"),
         ("about", "À propos"), ("contact", "Contact")]

def slug(p): return "accueil" if p == "" else p.replace("/", "-")

css = open(os.path.join(DIST, "assets", "site.css"), encoding="utf-8").read()

secs, nav = [], []
for p, label in PAGES:
    f = os.path.join(DIST, "index.html" if p == "" else f"{p}/index.html")
    s = open(f, encoding="utf-8").read()
    main = re.search(r'<main id="main">(.*?)</main>', s, re.S).group(1)
    # liens internes -> ancres de l'aperçu
    main = re.sub(r'href="/([^"#]*?)"',
                  lambda m: f'href="#{slug(m.group(1).strip("/"))}"', main)
    main = main.replace('href="/"', 'href="#accueil"')
    # les iframes YouTube ne sont pas autorisées dans un artifact : bloc explicatif
    main = re.sub(r'<div class="embed">.*?</div>',
        '<div class="embed placeholder"><p>Lecteur YouTube (playlist « uploads » de la '
        'chaîne, mise à jour automatique).<br><span>Actif sur le site déployé&nbsp;; '
        'les iframes externes sont bloquées dans cet aperçu.</span></p></div>',
        main, flags=re.S)
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', s, re.S).group(1)
    canon = re.search(r'<link rel="canonical" href="(.*?)">', s).group(1)
    secs.append(f"""<section class="page" id="{slug(p)}">
<div class="seo-strip">
  <p><span>URL</span> {html.escape(canon)}</p>
  <p><span>title</span> {html.escape(title)} <em>({len(title)} car.)</em></p>
  <p><span>description</span> {html.escape(desc)} <em>({len(desc)} car.)</em></p>
</div>
{main}
</section>""")
    nav.append(f'<li><a href="#{slug(p)}">{label}</a></li>')

doc = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Kyro / LoderPlayz — aperçu du site officiel</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@600;700&family=Inter+Tight:wght@400;500;600&display=swap">
<style>
{css}
body{{background-color:#140F20}}
.preview-head{{padding:1.4rem clamp(1rem,4vw,3rem);border-bottom:1px solid var(--edge)}}
.preview-head h1{{font:700 1.15rem/1.3 var(--disp);margin:0 0 .5rem}}
.preview-head p{{margin:0;color:var(--muted);font-size:.9rem}}
.preview-head ul{{display:flex;flex-wrap:wrap;gap:.3rem .9rem;list-style:none;padding:0;margin:.8rem 0 0}}
.preview-head a{{font-size:.9rem}}
.page{{padding:clamp(1.8rem,5vw,3.5rem) clamp(1rem,4vw,3rem) 3rem;max-width:74rem;margin:0 auto;
  border-bottom:8px solid var(--deep)}}
.seo-strip{{background:#0E0A18;border:1px solid var(--edge);padding:.9rem 1.1rem;margin-bottom:2.2rem;
  font-size:.82rem;line-height:1.5}}
.seo-strip p{{margin:.2rem 0;max-width:none;color:#C9C0E4;word-break:break-word}}
.seo-strip span{{display:inline-block;min-width:5.5rem;color:var(--gold);font-weight:600}}
.seo-strip em{{color:var(--muted);font-style:normal}}
.placeholder{{display:grid;place-items:center;text-align:center;aspect-ratio:16/9}}
.placeholder p{{margin:0;padding:1rem;color:var(--muted);font-size:.92rem;max-width:34ch}}
.placeholder span{{font-size:.82rem}}
</style></head><body>
<div class="preview-head">
<h1>Aperçu du site officiel Kyro / LoderPlayz</h1>
<p>Les 9 pages du site réel, empilées ici pour relecture. Le bandeau au-dessus de chaque
page montre l'URL, le title et la meta description qui seront servis.</p>
<ul>{''.join(nav)}</ul>
</div>
{''.join(secs)}
<footer class="foot"><p class="fine">Aperçu généré depuis dist/ — le site déployable est
livré séparément sous forme de fichiers statiques.</p></footer>
</body></html>"""

os.makedirs("/mnt/user-data/outputs", exist_ok=True)
open(OUT, "w", encoding="utf-8").write(doc)
print(f"[ok] {OUT} ({len(doc)//1024} Ko, {len(PAGES)} pages)")
