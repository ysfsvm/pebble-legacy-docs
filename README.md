# pebble-legacy-docs

Documentation site of the PebbleOS port to the legacy Pebble watches.

Build it:

```console
$ python3 -m venv .venv
$ .venv/bin/pip install -r requirements.txt
$ .venv/bin/sphinx-build -b html docs docs/_build/html
```

The pages are Markdown files under `docs/`. The theme, fonts and logo are
those of the [PebbleOS documentation](https://pebbleos.readthedocs.io).
