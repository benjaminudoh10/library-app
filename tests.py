import os
import unittest
from config import basedir
from library_app import app, db
from library_app.models import FeatureRequest, ProductArea, Client
from datetime import datetime
from flask import url_for
import json


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
         'sqlite:///' + os.path.join(basedir, 'feature-test.db')
        with app.app_context():
            self.app = app.test_client()
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_landing_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_feature_request(self):
        # check that post request for creating  feature request
        # is successful
        form_values = [
            {'name': 'title', 'value': 'Add pagination to the listing.'},
            {'name': 'description',
                'value': 'Feature that allows for the listing to be paginated.'},
            {'name': 'client', 'value': 'Client B'},
            {'name': 'client_priority', 'value': 3},
            {'name': 'target_date', 'value': '1993-11-16'},
            {'name': 'product_area', 'value': 'Policies'}
        ]
        response = self.app.post('/',
                                 data=json.dumps(form_values),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # check that ProductArea was created
        product_area = ProductArea.query.first()
        self.assertNotEqual(product_area, None)

        # check that Client was created
        client = Client.query.first()
        self.assertNotEqual(client, None)

        # check that all data are correct
        feature_request = FeatureRequest.query.first()
        self.assertNotEqual(feature_request, None)
        self.assertEqual(
            feature_request.title, 'Add pagination to the listing.')
        self.assertEqual(
            feature_request.description,
            'Feature that allows for the listing to be paginated.')
        self.assertEqual(feature_request.client.name, 'Client B')
        self.assertEqual(feature_request.client_priority, 3)
        self.assertEqual(feature_request.target_date,
                         datetime.strptime('1993-11-16', '%Y-%m-%d'))
        self.assertEqual(feature_request.product_area.name, 'Policies')

    def test_result_is_paginated(self):
        form_values = [
            [
                {'name': 'title', 'value': str(i)},
                {'name': 'description', 'value': str(i)},
                {'name': 'client', 'value': 'Client A'},
                {'name': 'client_priority', 'value': 1},
                {'name': 'target_date', 'value': '2018-01-30'},
                {'name': 'product_area', 'value': 'Policies'}
            ] for i in range(12)
        ]

        for item in form_values:
            response = self.app.post('/', data=json.dumps(item))
            self.assertEqual(response.status_code, 200)
        
        # check if page content is paginated
        response = self.app.get('/')
        self.assertIn('/?page=2', response.data)

    def test_client_priority_increments_by_1(self):
        form_values1 = [
            {'name': 'title', 'value': 'Add pagination to the listing.'},
            {
                'name': 'description',
                'value': 'Feature that allows for the listing to be paginated.'
            },
            {'name': 'client', 'value': 'Client A'},
            {'name': 'client_priority', 'value': 1},
            {'name': 'target_date', 'value': '2018-01-30'},
            {'name': 'product_area', 'value': 'Policies'}
        ]

        form_values2 = [
            {'name': 'title', 'value': 'Make use of Vue.js'},
            {'name': 'description', 'value': 'Use Vue.js as the frontend framework'},
            {'name': 'client', 'value': 'Client A'},
            {'name': 'client_priority', 'value': 1},
            {'name': 'target_date', 'value': '2019-11-21'},
            {'name': 'product_area', 'value': 'Claims'}
        ]

        form_values3 = [
            {'name': 'title', 'value': 'Facial Recognition'},
            {
                'name': 'description',
                'value': 'Make use of OpenCV to do some facial recognition tasks'
            },
            {'name': 'client', 'value': 'Client A'},
            {'name': 'client_priority', 'value': 1},
            {'name': 'target_date', 'value': '2019-10-11'},
            {'name': 'product_area', 'value': 'Billing'}
        ]
        
        response = self.app.post('/', data=json.dumps(form_values1))
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/', data=json.dumps(form_values2))
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/', data=json.dumps(form_values3))
        self.assertEqual(response.status_code, 200)

        # check that FeatureRequests created are three
        self.assertEqual(FeatureRequest.query.count(), 3)

        request1 = FeatureRequest.query.filter_by(id=1).one()
        request2 = FeatureRequest.query.filter_by(id=2).one()
        request3 = FeatureRequest.query.filter_by(id=3).one()

        # check feature request 1 has client priority of 3
        self.assertEqual(request1.client_priority, 3)
        # check feature request 2 has client priority of 2
        self.assertEqual(request2.client_priority, 2)
        # check feature request 3 has client priority of 1
        self.assertEqual(request3.client_priority, 1)

    def test_same_client_priority_isnt_shifted_with_diff_priority_num(self):
        form_values1 = [
            {'name': 'title', 'value': 'Make use of Vue.js'},
            {'name': 'description', 'value': 'Use Vue.js as the frontend framework'},
            {'name': 'client', 'value': 'Client A'},
            {'name': 'client_priority', 'value': 1},
            {'name': 'target_date', 'value': '2019-11-21'},
            {'name': 'product_area', 'value': 'Claims'}
        ]

        form_values2 = [
            {'name': 'title', 'value': 'Facial Recognition'},
            {
                'name': 'description',
                'value': 'Make use of OpenCV to do some facial recognition tasks'
            },
            {'name': 'client', 'value': 'Client A'},
            {'name': 'client_priority', 'value': 2},
            {'name': 'target_date', 'value': '2019-10-11'},
            {'name': 'product_area', 'value': 'Billing'}
        ]
        # create feature request by client A with client priority of 1
        response = self.app.post('/', data=json.dumps(form_values1))
        self.assertEqual(response.status_code, 200)

        # create feature request by client A with client priority of 2
        response = self.app.post('/', data=json.dumps(form_values2))
        self.assertEqual(response.status_code, 200)

        # check that FeatureRequests created are two
        self.assertEqual(FeatureRequest.query.count(), 2)

        # check feature request 1 has client priority of 1
        request1 = FeatureRequest.query.filter_by(id=1).one()
        self.assertEqual(request1.client_priority, 1)

        # check feature request 2 has client priority of 2
        request2 = FeatureRequest.query.filter_by(id=2).one()
        self.assertEqual(request2.client_priority, 2)

    def test_different_client_doesnt_shift_when_priority_same(self):
        form_values1 = [
            {'name': 'title', 'value': 'Make use of Vue.js'},
            {'name': 'description', 'value': 'Use Vue.js as the frontend framework'},
            {'name': 'client', 'value': 'Client A'},
            {'name': 'client_priority', 'value': 1},
            {'name': 'target_date', 'value': '2019-11-21'},
            {'name': 'product_area', 'value': 'Claims'}
        ]

        form_values2 = [
            {'name': 'title', 'value': 'Facial Recognition'},
            {
                'name': 'description',
                'value': 'Make use of OpenCV to do some facial recognition tasks'
            },
            {'name': 'client', 'value': 'Client B'},
            {'name': 'client_priority', 'value': 1},
            {'name': 'target_date', 'value': '2019-10-11'},
            {'name': 'product_area', 'value': 'Billing'}
        ]

        response = self.app.post('/', data=json.dumps(form_values1),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/', data=json.dumps(form_values2),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # check feature request 1 by client A has client priority of 1
        request1 = FeatureRequest.query.filter_by(id=1).one()
        self.assertEqual(request1.client_priority, 1)

        # check feature request 2 by client B has client priority of 1
        request2 = FeatureRequest.query.filter_by(id=2).one()
        self.assertEqual(request2.client_priority, 1)


if __name__ == "__main__":
    unittest.main()
