# Idle Desalination Facility

Official game website, available in English (default) and Spanish.

https://jafs6.github.io/idle-desalination-facility/

## Preview

Open `index.html` in a browser, or run `python -m http.server 8000` and visit http://localhost:8000/.

## Editing

- Pages: `scripts/templates/`.
- English translations: `scripts/translations.en.json`.
- Privacy policy: `content/privacy.es.md` and `content/privacy.en.md`.
- Styles, scripts and images: `assets/`.

After editing page content, regenerate the HTML:

```sh
python scripts/build.py
```

Commit the source and generated HTML together. Direct edits to generated HTML will be overwritten.

## Publishing

GitHub Pages: **Settings → Pages → Deploy from a branch → main → / (root)**.

Replace the temporary Google Play destination with the game's listing URL when available.

## Font

Barlow Semi Condensed is distributed under the [SIL Open Font License](assets/fonts/OFL.txt).