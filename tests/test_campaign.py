from twisted.internet import defer

import tests
from adpay.db import utils as db_utils

import copy


class InterfaceCampaignTestCase(tests.IfaceTestCase):
    CAMAPAIGN_DATA = {
        'campaign_id': 'campaign_id',
        'advertiser_id': 'advertiser_id',
        'time_start': 12345,
        'time_end': 34567,
        'filters': {},
        'keywords': {},
        'banners': [
            {
                'banner_id': 'banner1',
                'banner_size': '100x200',
                'keywords': {}
            },
            {
                'banner_id': 'banner2',
                'banner_size': '150x250',
                'keywords': {}
            }
        ],
        'max_cpc': 10,
        'max_cpm': 15,
        'budget': 1000
    }

    @defer.inlineCallbacks
    def test_add_campaign(self):
        response = yield self.get_response("campaign_update", [self.CAMAPAIGN_DATA])

        self.assertIsNotNone(response)
        self.assertTrue(response['result'])

        campaign_doc = yield db_utils.get_campaign(self.CAMAPAIGN_DATA['campaign_id'])
        self.assertIsNotNone(campaign_doc)
        self.assertEqual(campaign_doc['campaign_id'], self.CAMAPAIGN_DATA['campaign_id'])
        self.assertEqual(campaign_doc['budget'], 1000)

        campaign_banners = yield db_utils.get_campaign_banners(self.CAMAPAIGN_DATA['campaign_id'])
        self.assertEqual(len(campaign_banners), 2)
        for banner_doc in campaign_banners:
            self.assertIn(banner_doc['banner_id'], [elem['banner_id'] for elem in self.CAMAPAIGN_DATA['banners']])

    @defer.inlineCallbacks
    def test_change_campaign(self):
        changed_campaign_data = copy.deepcopy(self.CAMAPAIGN_DATA)
        changed_campaign_data['budget'] = 200
        changed_campaign_data['banners'] = [
            {
                'banner_id': 'changed',
                'banner_size': '100x200',
                'keywords': {}
            }
        ]

        response = yield self.get_response("campaign_update", [changed_campaign_data])
        self.assertIsNotNone(response)
        self.assertTrue(response['result'])

        campaign_doc = yield db_utils.get_campaign(changed_campaign_data['campaign_id'])
        self.assertIsNotNone(campaign_doc)
        self.assertEqual(campaign_doc['campaign_id'], changed_campaign_data['campaign_id'])
        self.assertEqual(campaign_doc['budget'], changed_campaign_data['budget'])

        campaign_banners = yield db_utils.get_campaign_banners(changed_campaign_data['campaign_id'])

        self.assertEqual(len(campaign_banners), 1)
        self.assertEqual(campaign_banners[0]['banner_id'], changed_campaign_data['banners'][0]['banner_id'])

    @defer.inlineCallbacks
    def test_delete_campaign(self):
        response = yield self.get_response("campaign_delete", [self.CAMAPAIGN_DATA['campaign_id']])

        self.assertIsNotNone(response)
        self.assertTrue(response['result'])

        campaign_doc = yield db_utils.get_campaign(self.CAMAPAIGN_DATA['campaign_id'])
        self.assertIsNone(campaign_doc)

        campaign_banners = yield db_utils.get_campaign_banners(self.CAMAPAIGN_DATA['campaign_id'])
        self.assertEqual(len(campaign_banners), 0)
