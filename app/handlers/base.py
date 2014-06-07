import webapp2
from services.response_renderer import ResponseRenderer


class BaseHandler(webapp2.RequestHandler, ResponseRenderer):
    def __init__(self, request, response):
        self.initialize(request, response)

    """Un-comment the code below if we need sessions in the future"""
    # def dispatch(self):
    #     self.session_store = sessions.get_store(request=self.request)
    #     try:
    #         webapp2.RequestHandler.dispatch(self)
    #     finally:
    #         self.session_store.save_sessions(self.response)
    #
    # @webapp2.cached_property
    # def session(self):
    #     return self.session_store.get_session()