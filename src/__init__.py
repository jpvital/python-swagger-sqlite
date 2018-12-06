from .shared import DB
from .app_config import APP
from .db.db_config import create_database

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

with APP.app.app_context():
    DB.init_app(APP.app)
    create_database()
