#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle qualité du dossier dist/ : JSON-LD, liens internes, SEO, sitemap."""
import json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")
errors, warns, ok = [], [], []

html_files = []
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".html"):
            html_files.append(os.path.join(d, f))

def rel(p): return os.path.relpath(p, ROOT)

def resolves(href):
    href = href.split("#")[0].split("?")[0]
    if not href.startswith("/"):
        return True  # externe ou ancre
    if href.endswith("/") or href == "/":
        return os.path.isfile(os.path.join(ROOT, href.strip("/"), "index.html")) or \
               (href == "/" and os.path.isfile(os.path.join(ROOT, "index.html")))
    p = os.path.join(ROOT, href.lstrip("/"))
    return os.path.isfile(p) or os.path.isfile(os.path.join(p, "index.html"))

canonicals, titles, descs = {}, {}, {}
for p in html_files:
    s = open(p, encoding="utf-8").read()
    name = rel(p)

    # JSON-LD
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            data = json.loads(m.group(1))
        except Exception as e:
            errors.append(f"{name}: JSON-LD invalide ({e})"); continue
        for node in data.get("@graph", []):
            if "@type" not in node:
                errors.append(f"{name}: nœud Schema sans @type")
        ok.append(f"{name}: JSON-LD valide ({len(data.get('@graph',[]))} nœuds)")

    # SEO de base
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    if not t: errors.append(f"{name}: pas de <title>")
    else:
        tt = t.group(1).strip()
        titles.setdefault(tt, []).append(name)
        if len(tt) > 65: warns.append(f"{name}: title {len(tt)} car. (>65, risque de troncature)")
    d = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
    if not d: errors.append(f"{name}: pas de meta description")
    else:
        dd = d.group(1).strip()
        descs.setdefault(dd, []).append(name)
        if not (70 <= len(dd) <= 165):
            warns.append(f"{name}: meta description {len(dd)} car. (cible 70-165)")
    c = re.search(r'<link rel="canonical" href="(.*?)">', s)
    if not c: errors.append(f"{name}: pas de canonical")
    else: canonicals.setdefault(c.group(1), []).append(name)

    h1 = re.findall(r"<h1[ >]", s)
    if len(h1) != 1: errors.append(f"{name}: {len(h1)} balise(s) H1 (il en faut 1)")

    if 'lang="fr"' not in s: errors.append(f"{name}: attribut lang manquant")
    if "og:title" not in s: errors.append(f"{name}: Open Graph manquant")

    # hiérarchie des titres : pas de H3 avant un H2
    order = re.findall(r"<h([1-3])[ >]", s)
    seen2 = False
    for lvl in order:
        if lvl == "2": seen2 = True
        if lvl == "3" and not seen2:
            warns.append(f"{name}: H3 avant tout H2")
            break

    # liens internes
    for href in re.findall(r'href="(/[^"]*)"', s):
        if not resolves(href):
            errors.append(f"{name}: lien interne cassé -> {href}")

    # iframes
    for ifr in re.findall(r"<iframe[^>]*>", s):
        if 'title="' not in ifr: errors.append(f"{name}: iframe sans title (accessibilité)")
        if 'loading="lazy"' not in ifr: warns.append(f"{name}: iframe sans loading=lazy")

for u, fs in canonicals.items():
    if len(fs) > 1: errors.append(f"canonical dupliqué {u} -> {fs}")
for t, fs in titles.items():
    if len(fs) > 1: errors.append(f"title dupliqué « {t} » -> {fs}")
for d, fs in descs.items():
    if len(fs) > 1: errors.append(f"meta description dupliquée -> {fs}")

# sitemap
sp = os.path.join(ROOT, "sitemap.xml")
if not os.path.isfile(sp): errors.append("sitemap.xml absent")
else:
    try:
        tree = ET.parse(sp)
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [e.text for e in tree.findall(".//s:loc", ns)]
        ok.append(f"sitemap.xml valide, {len(locs)} URL")
        canon = set(canonicals.keys())
        for l in locs:
            if l not in canon: errors.append(f"sitemap: {l} n'a pas de page canonique correspondante")
        for c in canon:
            if c not in locs and "/404" not in c:
                warns.append(f"page canonique absente du sitemap: {c}")
    except Exception as e:
        errors.append(f"sitemap.xml illisible: {e}")

# robots
rp = os.path.join(ROOT, "robots.txt")
if not os.path.isfile(rp): errors.append("robots.txt absent")
else:
    r = open(rp, encoding="utf-8").read()
    if "Sitemap:" not in r: errors.append("robots.txt sans directive Sitemap")
    if re.search(r"^Disallow: /$", r, re.M): errors.append("robots.txt bloque tout le site")
    else: ok.append("robots.txt cohérent")

# 404 en noindex
f404 = open(os.path.join(ROOT, "404.html"), encoding="utf-8").read()
if "noindex" not in f404: errors.append("404.html n'est pas en noindex")
else: ok.append("404.html en noindex")

print(f"Fichiers HTML analysés : {len(html_files)}")
print(f"\nOK ({len(ok)}) :")
for s in ok: print("  ✓", s)
print(f"\nAVERTISSEMENTS ({len(warns)}) :")
for s in warns: print("  !", s)
print(f"\nERREURS ({len(errors)}) :")
for s in errors: print("  ✗", s)
sys.exit(1 if errors else 0)
