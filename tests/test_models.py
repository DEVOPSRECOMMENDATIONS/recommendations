"""
Test cases for Recommendation Model

"""
import logging
import unittest
import os
from service.models import Recommendation, DataValidationError, db
from service import app

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
        recommendation = self._create_recommendation()
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
