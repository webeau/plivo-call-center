import logging
import plivoxml
from base import BaseHandler
# from main import db_helper

log = logging.getLogger(__name__)


class RoutingHandler(BaseHandler):
    def warm_up(self):
        log.info("This is enough of a warm up")
        self.render_text("Ready to go")

    def base_url(self):
        self.render_html("html/phone.html")

    def route(self):
        log.debug(self.request.params)

        response = plivoxml.Response()
        dial_params = dict(callerId=self.request.params.get("CallerName"))
        response.addDial(**dial_params).addUser("sip:vavagent1140607083814@phone.plivo.com")

        log.debug("Asking the call to do => "+str(response))

        self.response.headers['Content-Type'] = 'text/xml'
        self.response.write(str(response))

    def end(self):
        log.info(self.request.params)

    def message(self):
        log.info(self.request.params)