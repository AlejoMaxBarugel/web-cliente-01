#!/usr/bin/env python3
"""Completa el dominio en sitemap.xml, robots.txt e index.html.

Uso:   python configurar-dominio.py www.midominio.com.ar
(sin https:// y sin barra final). Se puede ejecutar más de una vez.
"""
import re, sys, pathlib

if len(sys.argv) != 2:
    sys.exit("Uso: python configurar-dominio.py www.midominio.com.ar")
dom = sys.argv[1].strip().lower()
dom = re.sub(r"^https?://", "", dom).strip("/")
if not re.fullmatch(r"[a-z0-9]([a-z0-9.-]*[a-z0-9])?\.[a-z]{2,}", dom):
    sys.exit("Dominio no válido: " + dom)
base = "https://" + dom
here = pathlib.Path(__file__).parent

# sitemap.xml y robots.txt (reemplaza el marcador o el dominio anterior)
for name in ("sitemap.xml", "robots.txt"):
    f = here / name
    t = f.read_text(encoding="utf-8")
    t = re.sub(r"https://[^/\s<]+(/sitemap\.xml|/(?=<))", lambda m: base + m.group(1), t)
    f.write_text(t, encoding="utf-8")

# index.html: canonical + vista previa al compartir (idempotente)
f = here / "index.html"
t = f.read_text(encoding="utf-8")
t = re.sub(r"<!-- dominio:inicio -->.*?<!-- dominio:fin -->\n?", "", t, flags=re.S)
bloque = (
    "<!-- dominio:inicio -->\n"
    f'<link rel="canonical" href="{base}/">\n'
    f'<meta property="og:url" content="{base}/">\n'
    f'<meta property="og:image" content="{base}/og-image.png">\n'
    '<meta property="og:image:width" content="1200">\n'
    '<meta property="og:image:height" content="630">\n'
    '<meta property="og:image:alt" content="JH - Instalaciones y Servicios Eléctricos en Mendoza">\n'
    f'<meta name="twitter:image" content="{base}/og-image.png">\n'
    "<!-- dominio:fin -->\n"
)
t = t.replace('<meta name="twitter:card" content="summary">', '<meta name="twitter:card" content="summary_large_image">')
t = t.replace("</head>", bloque + "</head>", 1)
f.write_text(t, encoding="utf-8")
print("Listo. Dominio configurado:", base)
