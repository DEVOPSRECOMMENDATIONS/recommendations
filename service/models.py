"""
Models for Recommendation

All of the models are stored in this module
"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Recommendation(db.Model):
    """
    Class that represents a <your resource model name>
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    product_a = db.Column(db.String(128), nullable=False)
    product_b = db.Column(db.String(128), nullable=False)
    recom_type = db.Column(db.String(1), nullable=False)
    

    def __repr__(self):
        return "<Recommendation %r id=[%s]>" % (self.product_a, self.id)

    def create(self):
        """
        Creates a Recommendation to the database
        """
        logger.info("Creating %s", self.product_a)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a Recommendation to the database
        """
        logger.info("Saving %s", self.product_a)
        db.session.commit()

    def delete(self):
        """ Removes a Recommendation from the data store """
        logger.info("Deleting %s", self.product_a)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Recommendation into a dictionary """
        return {
            "id": self.id,
            "product_a": self.product_a,
            "product_b": self.product_b,
            "recom_type": self.recom_type,
        }

    def deserialize(self, data):
        """
        Deserializes a Recommendation from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.product_a = data["product_a"]
            self.product_b = data["product_b"]
            self.recom_type = data["recom_type"]
        except KeyError as error:
            raise DataValidationError("Invalid Recommendation: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid Recommendation: body of request contained" "bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Recommendations in the database """
        logger.info("Processing all Recommendations")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a Recommendation by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a Recommendation by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, product_a):
        """ Returns all Recommendations with the given Product Name (product a)

        Args:
            name (string): the Product A of the Recommendations you want to match
        """
        logger.info("Processing Product A query for %s ...", product_a)
        return cls.query.filter(cls.product_a == product_a)
