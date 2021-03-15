"""
<your resource name> API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from service.models import db, Recommendation
from service.routes import app, init_db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendationServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db()


    def setUp(self):
        """ Runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_recommendation(self):
        return Recommendation(
            product_a="ProductA", 
            product_b="ProductB", 
            recom_type="U" 
        )

######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # data = resp.get_json()
        # self.assertEqual(data["name"], "Recommendation Demo REST API Service")

    def test_create_recommendation(self):
        """ Create a new Recommendation """
        test_recommendation = self._create_recommendation()
        logging.debug(test_recommendation)
        resp = self.app.post(
            "/recommendations", json=test_recommendation.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_recommendation = resp.get_json()
        self.assertEqual(new_recommendation["product_a"], test_recommendation.product_a)
        self.assertEqual(new_recommendation["product_b"], test_recommendation.product_b)
        self.assertEqual(new_recommendation["recom_type"], test_recommendation.recom_type)
        
        # ToDo: please uncomment once retrieve account is implemented

        # # Check that the location header was correct
        # resp = self.app.get(location, content_type="application/json")
        # self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # new_recommendation = resp.get_json()
        # self.assertEqual(new_recommendation["product_a"], test_recommendation.product_a)
        # self.assertEqual(new_recommendation["product_b"], test_recommendation.product_b)
        # self.assertEqual(new_recommendation["recom_type"], test_recommendation.recom_type)

    def test_update_recommendation(self):
        """ Update an existing Recommendation """
        # create a recommendation to update
        test_recommendation = self._create_recommendation()
        resp = self.app.post(
            "/recommendations", json=test_recommendation.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the recommendation
        new_recommendation = resp.get_json()
        logging.debug(new_recommendation)
        new_recommendation["product_a"] = "gloves"
        resp = self.app.put(
            "/recommendations/{}".format(new_recommendation["id"]),
            json=new_recommendation,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_recommendation = resp.get_json()
        self.assertEqual(updated_recommendation["product_a"], "gloves")

    def test_get_recommendation(self):
        """ Get a single Recommendation """
        # get the id of a recommendation
        test_recommendation = self._create_recommendation()
        test_recommendation.create()
        resp = self.app.get(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["product_a"], test_recommendation.product_a)
        self.assertEqual(data["product_b"], test_recommendation.product_b)
        self.assertEqual(data["recom_type"], test_recommendation.recom_type)

    def test_get_recommendation_not_found(self):
        """ Get a Recommendation thats not found """
        resp = self.app.get("/recommendations/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
