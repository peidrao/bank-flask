from importlib import import_module


def load_extensions(app):
    for ext in app.config["EXTENSIONS"]:
        try:
            mod = import_module(ext)
            mod.init_app(app)
        except Exception as e:
            print(f"Error loading extension '{ext}': {e}")


def init_app(app):
    app.config.from_object("config.settings")
