from mock import MagicMock, patch
from twisted.internet import defer

import tests
from adpay.db import utils as db_utils


class TestAddEvent(tests.WebTestCase):

    @defer.inlineCallbacks
    def test_no_campaign_add_event(self):

        cmp_doc = {"campaign_id": "campaign_id",
                   "time_start": 123,
                   "time_end": 234,
                   "max_cpc": 100,
                   "max_cpm": 100,
                   "budget": 1000,
                   "filters": {}}

        yield db_utils.update_campaign(cmp_doc)
        yield db_utils.update_banner({'banner_id': 'banner_1', 'campaign_id': 'campaign_id'})

        event_data = {
            'event_id': 'event_id',
            'event_type': 'event_type',
            'user_id': 'user_id',
            'human_score': 0.5,
            'publisher_id': 'publisher_id',
            'timestamp': 45678,
            'banner_id': "banner_1",
            'our_keywords': {},
            'their_keywords': {},
            'event_value': None
            }

        campaigns = MagicMock()
        campaigns.return_value = None

        with patch('adpay.db.utils.get_campaign', campaigns):
            response = yield self.get_response("add_events", [event_data])
            self.assertIsNotNone(response)
            self.assertTrue(response['result'])

        # Legacy add keywords
        with patch('adpay.db.utils.get_campaign', campaigns):
            response = yield self.get_response("add_events", [event_data])
            self.assertIsNotNone(response)
            self.assertTrue(response['result'])