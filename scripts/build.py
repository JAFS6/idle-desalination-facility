"""Generate the English and Spanish static pages using only Python's standard library."""
from pathlib import Path
import json
import posixpath
import re

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "scripts" / "templates"
ENGLISH = json.loads((ROOT / "scripts" / "translations.en.json").read_text(encoding="utf-8"))
PAGES = {"home": "index.html", "privacy": "privacy/index.html", "changelog": "changelog/index.html"}
SITE = "https://jafs6.github.io/idle-desalination-facility/"


def render_policy(locale):
    """Render the policy's small Markdown subset; escape text before adding markup."""
    from html import escape
    text = (ROOT / "content" / ("privacy." + locale + ".md")).read_text(encoding="utf-8")

    def inline(value):
        value = escape(value, quote=False)
        value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
        return re.sub(r"\[([^\]]+)\]\((https://[^\s)]+)\)",
                      lambda m: '<a href="' + escape(m[2], quote=True) + '">' + m[1] + '</a>', value)

    blocks = []
    for paragraph in re.split(r"\n\s*\n", text.strip()):
        if paragraph.startswith("# "):
            blocks.append("<h1>" + inline(paragraph[2:]) + "</h1>")
        elif paragraph.startswith("## "):
            title = paragraph[3:]
            number = re.match(r"(\d+)\.", title)
            anchor = ' id="privacy-section-' + number[1] + '"' if number else ""
            blocks.append("<h2" + anchor + ">" + inline(title) + "</h2>")
        elif paragraph.startswith("> "):
            blocks.append('<blockquote class="game-panel notice"><p>' + inline(paragraph[2:]) + '</p></blockquote>')
        else:
            pending = paragraph.startswith(("**[PENDIENTE", "**[TO COMPLETE"))
            style = ' class="policy-pending"' if pending else ""
            blocks.append("<p" + style + ">" + inline(paragraph) + "</p>")
    return "\n".join(blocks)

def render(name, locale, output):
    source = PAGES[name]
    html = (TEMPLATES / (name + ".html")).read_text(encoding="utf-8")
    if locale == "en":
        # One replacement pass avoids translating fragments of already translated text.
        pattern = "|".join(re.escape(text) for text in sorted(ENGLISH, key=len, reverse=True))
        html = re.sub(pattern, lambda match: ENGLISH[match.group()], html)
        html = re.sub(r'aria-label="(\d+) de (\d+)"', r'aria-label="\1 of \2"', html)
        html = re.sub(r"Ver captura (\d+):", r"View screenshot \1:", html)
    html = html.replace('<html lang="es">', '<html lang="' + locale + '">')
    if name == "privacy":
        html = html.replace("{{privacy_content}}", render_policy(locale))
    output_parent = posixpath.dirname(output) or "."

    def relative(target):
        return posixpath.relpath(target, output_parent)

    def rewrite(match):
        attribute, url = match.groups()
        if url.startswith(("https:", "mailto:", "#")):
            return match.group()
        path, separator, fragment = url.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
        if resolved in PAGES.values():
            resolved = locale + "/" + resolved
        return attribute + '="' + relative(resolved) + (separator + fragment if separator else "") + '"'

    html = re.sub(r'(href|src)="([^"]+)"', rewrite, html)
    equivalent_en = "en/" + source
    equivalent_es = "es/" + source
    language_label = "Language" if locale == "en" else "Idioma"
    switch = '        <div class="language-switch" role="group" aria-label="' + language_label + '">\n'
    for language, label, target in [("en", "English", equivalent_en), ("es", "Español", equivalent_es)]:
        current = ' aria-current="true"' if language == locale else ""
        switch += '          <a data-language-switch href="' + relative(target) + '" lang="' + language + '" hreflang="' + language + '"' + current + '>' + label + '</a>\n'
    switch += "        </div>\n"
    html = html.replace("      </div>\n    </nav>", switch + "      </div>\n    </nav>")
    metadata = '  <link rel="canonical" href="' + SITE + locale + '/' + source + '">\n'
    for language, target in [("en", equivalent_en), ("es", equivalent_es), ("x-default", equivalent_en)]:
        metadata += '  <link rel="alternate" hreflang="' + language + '" href="' + SITE + target + '">\n'
    html = html.replace("</head>", metadata + "</head>")
    destination = ROOT / output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html, encoding="utf-8", newline="\n")

for name, source in PAGES.items():
    for locale in ("en", "es"):
        render(name, locale, locale + "/" + source)
    # Preserve the original URLs and direct file preview, with English as the default.
    render(name, "en", source)
print("Generated 9 static pages: English defaults plus /en/ and /es/.")
