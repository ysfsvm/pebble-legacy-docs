# Sphinx configuration, kept close to PebbleOS' own documentation.

project = "PebbleOS for legacy watches"
copyright = "2026, the PebbleOS legacy port contributors"
author = "the PebbleOS legacy port contributors"

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

exclude_patterns = ["_build", "_templates"]
nitpicky = True

html_theme = "shibuya"
templates_path = ["_templates"]
html_static_path = ["_static"]
html_title = "PebbleOS for legacy watches"
html_favicon = "_static/images/favicon.svg"
html_css_files = ["css/custom.css"]
html_theme_options = {
    "light_logo": "_static/images/logo-light.svg",
    "dark_logo": "_static/images/logo-dark.svg",
    "accent_color": "tomato",
    "github_url": "https://github.com/ysfsvm/PebbleOS-legacy",
    "nav_links": [
        {"title": "Use", "url": "use/watches"},
        {"title": "Develop", "url": "develop/build"},
        {"title": "PebbleOS documentation", "url": "https://pebbleos.readthedocs.io/latest/"},
    ],
}
html_context = {
    "source_type": "github",
    "source_user": "ysfsvm",
    "source_repo": "pebble-legacy-docs",
    "source_version": "main",
    "source_docs_path": "/docs/",
}

copybutton_prompt_text = r"\$ "
copybutton_prompt_is_regexp = True
