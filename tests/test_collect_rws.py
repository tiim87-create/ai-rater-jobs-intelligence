import unittest
from scripts.collect_rws import transform,validate,country
class Tests(unittest.TestCase):
    def test_language_not_country(self):
        x=transform({"id":"1","text":"Bengali Evaluator","categories":{"location":"Remote"}})
        self.assertEqual(x["countries"],[])
    def test_location_and_workplace(self):
        x=transform({"id":"2","text":"Evaluator","categories":{"location":"London, UK"},"workplaceType":"remote"})
        self.assertEqual(x["countries"],["GB"])
        self.assertEqual(x["workplace_type"],"remote")
    def test_duplicate(self):
        x=transform({"id":"2","categories":{"location":"India"}})
        self.assertTrue(validate([x,x],[],1,.2,.35)[0])
    def test_bad_feed(self):
        x=transform({"id":"3","categories":{"location":"Remote"}})
        self.assertTrue(validate([x],[],1,.2,.35)[0])
if __name__=="__main__":unittest.main()
