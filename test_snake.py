import unittest
from snake_game import *
import snake_game


class ComplexTestCase(unittest.TestCase):
    def test_snake_eat_food(self):
        if snake_game.sprite.collide_rect(snake, food):
            assert food_collide_snake is True

    def test_snake_eat_bad_food(self):
        if snake_game.sprite.collide_rect(snake, bad_food):
            assert bad_food_collide_snake is True


def suite():
    suite = unittest.TestSuite()
    suite.addTest(ComplexTestCase("test_snake_eat_food"))
    suite.addTest(ComplexTestCase("test_snake_eat_bad_food"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
