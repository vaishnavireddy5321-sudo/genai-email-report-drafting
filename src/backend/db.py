"""Database initialization and setup for the GenAI Email & Report Drafting System.

This module initializes the SQLAlchemy database instance and provides
utilities for database management.
"""

import sqlite3

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Initialize Flask-Migrate instance
migrate = Migrate()


@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, _connection_record):
    """Enable SQLite foreign key support for ON DELETE behavior."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def init_db(app):
    """Initialize database with Flask application.

    Args:
        app: Flask application instance
    """
    db.init_app(app)
    migrate.init_app(app, db)


def create_tables(app):
    """Create all database tables.

    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.create_all()


def drop_tables(app):
    """Drop all database tables.

    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.drop_all()
