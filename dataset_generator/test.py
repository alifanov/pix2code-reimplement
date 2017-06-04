import sys
sys.path.append('.')

import unittest
import numpy as np
from html_renderer import HTMLGame
from html2vec.converter import HTML2VECConverter
from PIL import Image

TEST_HTML = '<body><p>PText</p></body>'


class HTMLGameTestCase(unittest.TestCase):
    def test_html_game_step(self):
        res_image = Image.open('test_render.png')
        game = HTMLGame(result_image=res_image)
        converter = HTML2VECConverter()
        state, reward, done = game.step(converter.convert(TEST_HTML))
        self.assertEqual(reward, 1.0)
        self.assertEqual(done, True)

if __name__ == '__main__':
    unittest.main()
