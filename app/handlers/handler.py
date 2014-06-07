import logging
import plivoxml
import plivo
from base import BaseHandler
from main import db_helper
from sqlalchemy.orm.exc import NoResultFound

log = logging.getLogger(__name__)


class RoutingHandler(BaseHandler):
    def warm_up(self):
        log.info("This is enough of a warm up")
        self.render_text("Ready to go")

    def base_url(self):
        self.render_html("html/phone.html")

    def get_active_calls(self):
        self.render_json(dict(count=db_helper.get_active_calls_from_queue()))

    def route(self):
        log.debug(self.request.params)
        request_params = self.request.params.copy()
        response = plivoxml.Response()


        agent = db_helper.get_available_agent()
        if agent:
            agent.OnCall = True
            db_helper.session.commit()

            request_params.update({"Agent":agent.Id})
            dial_params = dict(callerId=self.request.params.get("CallerName"))
            response.addDial(**dial_params).addUser("sip:"+agent.Id+"@phone.plivo.com")
        else:
            play_params = dict(loop="0")
            response.addPlay("http://www.mohsamples.com/music/9a1f30943126974075dbd4d13c8018ac/Bikes%20Two.mp3", **play_params)

        db_helper.save_inbound_call_details(request_params)
        log.debug("Asking the call to do => "+str(response))

        self.response.headers['Content-Type'] = 'text/xml'
        self.response.write(str(response))

    def end(self):
        try:
            call = db_helper.get_call_by_id(self.request.params.get("CallUUID"))
            call.IsCompleted = True
            db_helper.session.commit()

            agent_id = call.Agent
        except NoResultFound:
            log.error("Thats no good. Where did "+self.request.params.get("CallUUID")+" go?")
            return


        agent = db_helper.get_agent_by_id(agent_id)
        agent.OnCall = False

        call = db_helper.get_call_from_queue()
        if call:
            log.info(call.to_dict())
            call.Agent = agent_id
            params = dict(aleg_url="https://go-for-plivo.appspot.com/route", aleg_method="POST")
            response = plivo.RestAPI("MAMWQ3MJCWMJI0ZME5MD","ZDNhYmZhY2U4NWRlNGY2MGI4MzMwZjQxZGZjZWJh").Call.transfer(call.Id, **params)
            log.info(response)
        # else:

        db_helper.session.commit()

    def message(self):
        log.info(self.request.params)



class AgentHandler(BaseHandler):

    def post(self):
        self.render_json(db_helper.agent_login(self.request.params))
        call = db_helper.get_call_from_queue()
        if call:
            call.Agent = self.request.params.get("Id")
            params = dict(aleg_url="https://go-for-plivo.appspot.com/route", aleg_method="POST")
            response = plivo.RestAPI("MAMWQ3MJCWMJI0ZME5MD","ZDNhYmZhY2U4NWRlNGY2MGI4MzMwZjQxZGZjZWJh").Call.transfer(call.Id, **params)
            log.info(response)
        db_helper.session.commit()


    def delete(self, id):
        db_helper.agent_logout(id)