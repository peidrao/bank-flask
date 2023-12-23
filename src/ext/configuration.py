from importlib import import_module


def load_extensions(app):
    for ext in app.config.get("EXTENSIONS"):
        mod = import_module(ext)
        mod.init_app(app)


def init_app(app):
    app.config.from_object("config.settings")
