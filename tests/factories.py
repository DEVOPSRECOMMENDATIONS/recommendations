"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from service.models import Recommendation


class RecommendationFactory(factory.Factory):
    """ Creates fake recommendations that you don't have to feed """

    class Meta:
        model = Recommendation

    id = factory.Sequence(lambda n: n)
    product_a = FuzzyChoice(choices=["gloves", "shoes", "hats", "belts"])
    product_b = FuzzyChoice(choices=["socks", "pants", "skirts", "dresses"])
    recom_type = FuzzyChoice(choices=["A", "B", "C"])