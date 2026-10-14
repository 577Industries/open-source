# Vendored fonts (SIL OFL 1.1)

Static instances used by `../build.mjs` (satori requires static weights).
Sources: [google/fonts](https://github.com/google/fonts) — OFL license texts alongside.

Regenerate statics from the upstream variable fonts with:

```bash
pip install fonttools
fonttools varLib.instancer "InterTight[wght].ttf" wght=400   # etc. for 500/600
fonttools varLib.instancer "JetBrainsMono[wght].ttf" wght=400 # etc. for 500/700
```
