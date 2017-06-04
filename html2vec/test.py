import unittest
from converter import HTML2VECConverter

TEST_HTML = """
<html>
<body>
<div>
    <button>Click me</button>
</div>
<div>
    <input />
</div>
</body>
</html>
"""

TEST_SPLIT = ['<html', '>', '<body', '>', '<div', '>', '<button', '>', '</button>', '</div>',
              '<div', '>', '<input', '/>', '</div>', '</body>', '</html>']

TEST_VEC = [18, 2, 3, 2, 9, 2, 13, 2, 14, 10, 9, 2, 5, 1, 10, 4, 19]

TEST_REVERSED_HTML = '<html><body><div><button></button></div><div><input/></div></body></html>'


class HTML2VECTestCase(unittest.TestCase):
    def test_split_html(self):
        c = HTML2VECConverter()
        l = c.split_html(TEST_HTML)
        self.assertEqual(l, TEST_SPLIT)

    def test_convert_html2vec(self):
        c = HTML2VECConverter()
        vec = c.convert(TEST_HTML)
        self.assertEqual(vec, TEST_VEC)

    def test_convert_vec2html(self):
        c = HTML2VECConverter()
        html = c.convert(TEST_VEC, direction=HTML2VECConverter.VEC2HTML_DIRECTION)
        self.assertEqual(html, TEST_REVERSED_HTML)


if __name__ == '__main__':
    unittest.main()
