import unittest
import webapp2
import json
import time
from google.appengine.ext import testbed


class AgentHandlerTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        from main import app
        self.app = app

    def test_agent_login(self):
        params = dict(Id="abc")
        request = webapp2.Request.blank('/agent', POST=params)
        response = request.get_response(self.app)

        self.assertEqual(response.status, "200 OK")

        response_dict = json.loads(response.body)

        self.assertIsNotNone(response_dict.get("Id"))

        time.sleep(1)

        current_time = response_dict.get("DateAdded")

        request = webapp2.Request.blank('/agent', POST=params)
        response = request.get_response(self.app)
        response_dict = json.loads(response.body)

        self.assertNotEqual(current_time, response_dict.get("DateAdded"))

        def tearDown(self):
            self.testbed.deactivate()



class CallHandlerTest(unittest.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        from main import app
        self.app = app

    def test_send_sample_call(self):
        params = dict(Direction='inbound',
                           From='919884038953',
                           CallerName='+919884038953',
                           BillRate='0.00850',
                           To='15033896659',
                           CallUUID='81d93d74-ee2e-11e3-823b-9df84a39ec44',
                           CallStatus='ringing',
                           Event='StartApp')
        request = webapp2.Request.blank('/route', POST=params)
        response = request.get_response(self.app)
        self.assertNotEqual(-1, response.body.index("abc"))

        params = dict(Direction='inbound',
                           From='919884038953',
                           CallerName='+919884038953',
                           BillRate='0.00850',
                           To='15033896659',
                           CallUUID='81d93d74-eesdfsdf3-823b-9df84a39ec44',
                           CallStatus='ringing',
                           Event='StartApp')
        request = webapp2.Request.blank('/route', POST=params)
        response = request.get_response(self.app)
        self.assertNotEqual(-1, response.body.index("Bikes"))

    def tearDown(self):
        self.testbed.deactivate()

