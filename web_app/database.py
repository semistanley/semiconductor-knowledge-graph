from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import settings

db = SQLAlchemy()
migrate = Migrate()


def init_db(app) -> None:
    uri = settings.get_sqlalchemy_uri()
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }
    app.config["SECRET_KEY"] = settings.FLASK_SECRET_KEY
    if "sqlalchemy" not in app.extensions:
        db.init_app(app)
        migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
