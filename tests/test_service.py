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
from service.routes import app, init_db
from .factories import RecommendationFactory
from service.models import db, Recommendation, DataValidationError
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

    def _create_recommendation_array(self, count):
        recommendations = []
        for _ in range(count):
            test_recommendation = RecommendationFactory()
            resp = self.app.post(
                '/recommendations', json=test_recommendation.serialize(), content_type='application/json'
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test recommendation"
            )
            new_recommendation= resp.get_json()
            test_recommendation.id = new_recommendation["id"]
            recommendations.append(test_recommendation)
        return recommendations

    def _create_recommendation(self):
        return Recommendation(
            product_a="ProductA", 
            product_b="ProductB", 
            recom_type="U", 
            likes=0
        )
######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()

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

    def test_list_recommendation(self):
        """ Get a list of Recommendations """
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.create()
        resp = self.app.get("/recommendations")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 1)

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

    def test_delete_recommendation(self):
        """ Delete a Recommendation """
        test_recommendation = self._create_recommendation()
        test_recommendation.create()
        resp = self.app.delete(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

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



    def test_like_recommendation(self):
        """ Like a Recommendation """
        # create a recommendation to like
        test_recommendation = self._create_recommendation()
        resp = self.app.post(
            "/recommendations", json=test_recommendation.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        
        # like the recommendation
        new_recommendation = resp.get_json()
        logging.debug(new_recommendation)
        self.assertEqual(new_recommendation["likes"], 0)
        resp = self.app.put(
            "/recommendations/{}/likes".format(new_recommendation["id"]),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        likes_count = resp.get_json()
        logging.debug(likes_count)
        self.assertEqual(likes_count["likes"], 1)


    def test_query_by_product_A(self):
        """ Query Recommendations by Product A """
        test_recommendation = self._create_recommendation()
        test_recommendation.create()
        resp = self.app.get(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertIn(b'ProductA', resp.data)
        self.assertNotIn(b'hats', resp.data)
        data = resp.get_json()
        logging.debug('data = %s', data)
        self.assertEqual(data["product_a"], test_recommendation.product_a)


    def test_query_by_product_B(self):
        """ Query Recommendations by Product B """
        test_recommendation = self._create_recommendation()
        test_recommendation.create()
        resp = self.app.get(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertIn(b'ProductB', resp.data)
        self.assertNotIn(b'hats', resp.data)
        data = resp.get_json()
        logging.debug('data = %s', data)
        self.assertEqual(data["product_b"], test_recommendation.product_b)


    def test_query_by_Recom_Type(self):
        """ Query Recommendations by Recommendation Type """
        test_recommendation = self._create_recommendation()
        test_recommendation.create()
        resp = self.app.get(
            "/recommendations/{}".format(test_recommendation.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertIn(b'recom_type', resp.data)
        self.assertNotIn(b'hats', resp.data)
        data = resp.get_json()
        logging.debug('data = %s', data)
        self.assertEqual(data["recom_type"], test_recommendation.recom_type)


    def test_get_recommendation_not_found(self):
        """ Get a Recommendation thats not found """
        resp = self.app.get("/recommendations/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_deserialize_missing_data(self):
        """ Test deserialization of a Reommendation """
        data = {"id": 1, "product_a:":"shoes", "product_b":"belts", "recom_type":"A"}
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)
        
    def test_create_recommendation_no_content_type(self):
        """ Create a new Recommendation without content type """
        test_recommendation = RecommendationFactory()
        resp = self.app.post('/recommendations',
                             json=test_recommendation.serialize(),
                             content_type="bad content")
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_query_recommendation_list_by_recomm_Type(self):
        """ Query Recommendations by Category """
        recommendations = self._create_recommendation_array(10)
        test_recom_type = recommendations[0].recom_type
        category_recommendations = [recommendations for recommendation in recommendations if recommendation.recom_type == test_recom_type]
        resp = self.app.get('/recommendations', query_string="recom_type={}".format(test_recom_type))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["recom_type"], test_recom_type)
    
    def test_query_recommendation_list_by_Product_A(self):
        """ Query Recommendations by Product A """
        recommendations = self._create_recommendation_array(10)
        test_product_a = recommendations[0].recom_type
        category_recommendations = [recommendations for recommendation in recommendations if recommendation.product_a == test_product_a]
        resp = self.app.get('/recommendations', query_string="product_a={}".format(test_product_a))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["product_a"], test_product_a)

    def test_query_recommendation_list_by_Product_B(self):
        """ Query Recommendations by Product B """
        recommendations = self._create_recommendation_array(10)
        test_product_b = recommendations[0].recom_type
        category_recommendations = [recommendations for recommendation in recommendations if recommendation.product_b == test_product_b]
        resp = self.app.get('/recommendations', query_string="product_b={}".format(test_product_b))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_recommendations))
        # check the data just to be sure
        for recommendation in data:
            self.assertEqual(recommendation["product_b"], test_product_b)
            
            

