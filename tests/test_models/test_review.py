#!/usr/bin/python3

import unittest
import os

from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rev1 = Review()
        cls.rev1.place_id = "Hong Kong"
        cls.rev1.user_id = "Kim Yung"
        cls.rev1.text = "Arigatou"

    @classmethod
    def tearDownClass(cls):
        del cls.rev1
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_is_subclass(self):
        self.assertTrue(issubclass(self.rev1.__class__, BaseModel), True)

    def test_checking_for_functions(self):
        self.assertIsNotNone(Review.__doc__)

    def test_has_attributes(self):
        self.assertTrue('id' in self.rev1.__dict__)
        self.assertTrue('created_at' in self.rev1.__dict__)
        self.assertTrue('updated_at' in self.rev1.__dict__)
        self.assertTrue('place_id' in self.rev1.__dict__)
        self.assertTrue('text' in self.rev1.__dict__)
        self.assertTrue('user_id' in self.rev1.__dict__)

    def test_attributes_are_strings(self):
        self.assertEqual(type(self.rev1.text), str)
        self.assertEqual(type(self.rev1.place_id), str)
        self.assertEqual(type(self.rev1.user_id), str)

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db',
        "won't work in db")
    def test_save(self):
        self.rev1.save()
        self.assertNotEqual(self.rev1.created_at, self.rev1.updated_at)

    def test_to_dict(self):
        self.assertEqual('to_dict' in dir(self.rev1), True)


if __name__ == "__main__":
    unittest.main()
