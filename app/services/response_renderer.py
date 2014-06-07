import os
import json
import logging
from helper import ComplexEncoder

log = logging.getLogger(__name__)


class ResponseRenderer(object):
    """Different types of responses"""

    def __init__(self, arg):
        super(ResponseRenderer, self).__init__()

    def render_unauthorized(self):
        self.response.status = 401
        self.response.headers['Content-Type'] = 'application/json'
        self.render_json({'response': 401})

    def render_html(self, _template):
        tmpl = os.path.join(os.path.dirname(__file__), "../"+_template)
        template_content = open(tmpl, 'r').read()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template_content)

    def render_json(self, obj):
        rv = json.dumps(obj, cls=ComplexEncoder)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(rv)

    def render_text(self, obj):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(obj)