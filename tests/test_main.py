import unittest
from main import QuizApp

class TestQuizApp(unittest.TestCase):
    def setUp(self):
        self.app = QuizApp(None)

    def test_is_similar(self):
        self.assertTrue(self.app.is_similar("brsila", "brasília"))
        self.assertFalse(self.app.is_similar("abc", "xyz"))

if __name__ == "__main__":
    unittest.main()
