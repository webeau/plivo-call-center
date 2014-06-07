import unittest
import webapp2
from google.appengine.ext import testbed

sample_inbound_call = dict(Direction='inbound',
                           From='919884038953',
                           CallerName='+919884038953',
                           BillRate='0.00850',
                           To='15033896659',
                           CallUUID='81d93d74-ee2e-11e3-823b-9df84a39ec44',
                           CallStatus='ringing',
                           Event='StartApp')

class ChannelHandlerTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        from main import app
        self.app = app

    def test_send_sample_call(self):
        request = webapp2.Request.blank('/route', POST=sample_inbound_call)
        response = request.get_response(self.app)
        print response

    def tearDown(self):
        self.testbed.deactivate()