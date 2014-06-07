import logging
from config import app_config
from models.sql_schema import Base, AgentPresence, CallQueue
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from sqlalchemy import desc, and_
from sqlalchemy.orm.exc import NoResultFound


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

    def save_inbound_call_details(self, params):
        call = self.session.query(CallQueue).filter_by(Id=params.get("CallUUID")).first()
        if call is not None:
            return
        call = CallQueue()
        call.Id = params.get("CallUUID")
        call.Direction = params.get("Direction")
        call.From = params.get("From")
        call.CallerName = params.get("CallerName")
        call.BillRate = params.get("BillRate")
        call.To = params.get("To")
        call.CallStatus = params.get("CallStatus")
        call.Event = params.get("Event")
        call.Agent = params.get("Agent")
        call.IsCompleted = False
        self.session.add(call)
        self.session.commit()

    def get_call_from_queue(self):
        call = self.session.query(CallQueue).filter(and_(CallQueue.IsCompleted==False,CallQueue.Agent==None)).order_by(desc(CallQueue.QueueTime)).first()
        return call

    def get_active_calls_from_queue(self):
        calls = self.session.query(CallQueue).filter(and_(CallQueue.IsCompleted==False,CallQueue.Agent==None)).all()
        return len(calls)

    def get_call_by_id(self, Id):
        call = self.session.query(CallQueue).filter_by(Id=Id).one()
        return call

    def get_agent_by_id(self, Id):
        agent = self.session.query(AgentPresence).filter_by(Id=Id).one()
        return agent

    def agent_login(self, params):
        agent = None
        agent_list = self.session.query(AgentPresence).filter_by(Id=params.get("Id")).all()
        if not agent_list:
            agent = AgentPresence()
            agent.Id = params.get("Id")
            agent.DateAdded = datetime.now()
            self.session.add(agent)
        elif len(agent_list) is 1:
            agent = agent_list[0]
            agent.DateAdded = datetime.now()
        self.session.commit()
        return agent.to_dict()

    def agent_logout(self, id):
        agent_presence = self.session.query(AgentPresence).filter_by(Id=id).all()
        if agent_presence:
            [self.session.delete(agent) for agent in agent_presence]
            self.session.commit()

    def get_available_agent(self):
        return self.session.query(AgentPresence).filter_by(OnCall=False).first()