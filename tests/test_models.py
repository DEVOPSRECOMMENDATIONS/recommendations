"""
Test cases for Recommendation Model

"""
import logging
import unittest
import os
from .factories import RecommendationFactory
from service.models import Recommendation, DataValidationError, db
from service import app
from werkzeug.exceptions import NotFound

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  R E C O M M E N D A T I O N S  M O D E L   T E S T   C A S E S
######################################################################
class TestRecommendation(unittest.TestCase):
    """ Test Cases for Recommendations Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Recommendation.init_db(app)

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
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

    def test_create_a_recommendation(self):
        """ Create a recommendation and assert that it exists """
        recommendation = self._create_recommendation()
        self.assertTrue(recommendation != None)
        self.assertEqual(recommendation.id, None)
        self.assertEqual(recommendation.product_a, "ProductA")
        self.assertEqual(recommendation.product_b, "ProductB")
        self.assertEqual(recommendation.recom_type, "U")


    def test_add_a_recommendation(self):
        """ Create a recommendation and add it to the database """
        recommendations = Recommendation.all()
        self.assertEqual(recommendations, [])

        recommendation = self._create_recommendation()
        
        self.assertTrue(recommendation != None)
        self.assertEqual(recommendation.id, None)
        recommendation.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertNotEqual(recommendation.id, None)
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        recommendation = Recommendation()
        self.assertRaises(DataValidationError, recommendation.deserialize, data)       

    def test_update_a_recommendation(self):
        """ Update a Recommendation """
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.create()
        logging.debug(recommendation)
        self.assertEqual(recommendation.id, 1)
        # Change it an save it
        recommendation.product_b = "shoes"
        original_id = recommendation.id
        recommendation.save()
        self.assertEqual(recommendation.id, original_id)
        self.assertEqual(recommendation.product_b, "shoes")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        recommendations = Recommendation.all()
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0].id, 1)
        self.assertEqual(recommendations[0].product_b, "shoes")

    def test_delete_a_recommendation(self):
        """ Delete a Recommendation """
        recommendation = RecommendationFactory()
        logging.debug(recommendation)
        recommendation.create()
        self.assertEqual(len(Recommendation.all()), 1)
        # delete the recommendation  and make sure it isn't in the database
        recommendation.delete()
        self.assertEqual(len(Recommendation.all()), 0)

    def test_find_recommendation(self):
        """ Find a Recommendation by ID """
        recommendations = RecommendationFactory.create_batch(3)
        for recommendation in recommendations:
            recommendation.create()
        logging.debug(recommendations)
        # make sure they got saved
        self.assertEqual(len(Recommendation.all()), 3)
        # find the 2nd recommendation in the list
        recommendation = Recommendation.find(recommendations[1].id)
        self.assertIsNot(recommendation, None)
        self.assertEqual(recommendation.id, recommendations[1].id)
        self.assertEqual(recommendation.product_a, recommendations[1].product_a)
        self.assertEqual(recommendation.product_b, recommendations[1].product_b)
        self.assertEqual(recommendation.recom_type, recommendations[1].recom_type)

    def test_find_or_404_found(self):
        """ Find or return 404 found """
        recommendations = RecommendationFactory.create_batch(3)
        for recommendation in recommendations:
            recommendation.create()

        recommendation = Recommendation.find_or_404(recommendations[1].id)
        self.assertIsNot(recommendation, None)
        self.assertEqual(recommendation.id, recommendations[1].id)
        self.assertEqual(recommendation.product_a, recommendations[1].product_a)
        self.assertEqual(recommendation.product_b, recommendations[1].product_b)
        self.assertEqual(recommendation.recom_type, recommendations[1].recom_type)

    def test_find_or_404_not_found(self):
        """ Find or return 404 NOT found """
        self.assertRaises(NotFound, Recommendation.find_or_404, 0)

    def test_find_by_product_a(self):
        """ Find a Recommendation by Product Name A"""
        Recommendation(product_a="shoes", product_b="belts", recom_type="A").create()
        Recommendation(product_a="shoes", product_b="skirts", recom_type="B").create()
        Recommendation(product_a="shoes", product_b="gloves", recom_type="B").create()
        recommendations = Recommendation.find_by_product_a("shoes")
        recommendation_list = [recommendation for recommendation in recommendations]
        self.assertEqual(len(recommendation_list), 3)

    def test_find_by_product_b(self):
        """ Find a Recommendation by Product Name B"""
        Recommendation(product_a="shirts", product_b="shirts", recom_type="A").create()
        Recommendation(product_a="shoes", product_b="skirts", recom_type="B").create()
        Recommendation(product_a="shoes", product_b="gloves", recom_type="B").create()
        recommendations = Recommendation.find_by_product_b("shirts")
        recommendation_list = [recommendation for recommendation in recommendations]
        self.assertEqual(len(recommendation_list), 1)
    
    def test_find_by_recommendation_type(self):
        """ Find Recommendations by Recommendation Type """
        Recommendation(product_a="shoes", product_b="belts", recom_type="A").create()
        Recommendation(product_a="shoes", product_b="skirts", recom_type="A").create()
        Recommendation(product_a="shirts", product_b="pants", recom_type="A").create()
        recommendations = Recommendation.find_by_recommendation_type("A")
        recommendation_list = [recommendation for recommendation in recommendations]
        self.assertEqual(len(recommendation_list), 3)

    def test_find_by_recommendation_type_and_product_a(self):
        """ Find Recommendations by Recommendation Type and Product A"""
        Recommendation(product_a="shoes", product_b="belts", recom_type="A").create()
        Recommendation(product_a="skirts", product_b="shoes", recom_type="B").create()
        Recommendation(product_a="pants", product_b="belts", recom_type="B").create()
        recommendations = Recommendation.find_by_recommendation_type_and_product_a("B","pants")
        recommendation_list = [recommendation for recommendation in recommendations]
        self.assertEqual(len(recommendation_list), 1)

    def test_find_by_recommendation_type_and_product_b(self):
        """ Find Recommendations by Recommendation Type and Product B"""
        Recommendation(product_a="skirts", product_b="belts", recom_type="B").create()
        Recommendation(product_a="gloves", product_b="belts", recom_type="B").create()
        Recommendation(product_a="shirt", product_b="belts", recom_type="B").create()
        recommendations = Recommendation.find_by_recommendation_type_and_product_b("B","belts")
        recommendation_list = [recommendation for recommendation in recommendations]
        self.assertEqual(len(recommendation_list), 3)