from twisted.internet import defer

from adpay.iface.tests import IfaceTestCase
from adpay.db import utils as db_utils


class InterfacePaymentTestCase(IfaceTestCase):
    @defer.inlineCallbacks
    def test_get_payments(self):
        response = yield self.get_response("get_payments", [{'timestamp':0}])
        self.assertIsNotNone(response)
        self.assertEqual(response['result']['payments'], [])

        # Add some dummy payments.
        yield db_utils.update_payment_round(7200)
        for i in range(100):
            yield db_utils.update_event_payment("campaign_id", 7200, "event_%s"%i, 100)

        response = yield self.get_response("get_payments", [{'timestamp':7200}])
        self.assertIsNotNone(response)
        self.assertEqual(len(response['result']['payments']), 100)

        for index, payment in enumerate(response['result']['payments']):
            self.assertEqual(payment['amount'], 100)
            self.assertEqual(payment['event_id'], 'event_%s'%index)


        response = yield self.get_response("get_payments", [{'timestamp':3600}])
        self.assertIsNotNone(response)
        self.assertEqual(response['result']['payments'], [])

        response = yield self.get_response("get_payments", [{'timestamp':7210}])
        self.assertIsNotNone(response)
        self.assertEqual(response['result']['payments'], [])

        response = yield self.get_response("get_payments", [{'timestamp':6500}])
        self.assertIsNotNone(response)
        self.assertEqual(len(response['result']['payments']), 100)
