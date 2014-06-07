import logging
from config import app_config
from models.sql_schema import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


log = logging.getLogger(__name__)

class DBHelper(object):

    def __init__(self, engine=None):
        log.debug("New instance of the database helper created")
        log.debug("Lets hope to god that this is also a new instace of the appengine app")

        if not engine:
            kwargs = {}
            if app_config["DB_POOL_RECYCLE"] is not None: kwargs["pool_recycle"] = app_config["DB_POOL_RECYCLE"]
            engine = create_engine(app_config['DB_STRING'], **kwargs)
            engine.echo = app_config["DB_DEBUG"]

        self.engine = engine
        self.session = scoped_session(sessionmaker(bind=self.engine))

        Base.metadata.create_all(bind=engine)
        log.debug("Tables schemas created and updated")

    def save_inbound_call_details(self):
        pass

    def save_agent_login(self):
        pass