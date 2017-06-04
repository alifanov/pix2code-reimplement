import random
import sys, os
sys.path.append('..')

from scipy.spatial import distance
from html2vec.converter import HTML2VECConverter
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtCore import *
from PIL import Image


def decode_state(state):
    return [np.argmax(v) for v in np.split(state[0], 3)]


class HTMLRenderer(QWebView):
    """
    Renderer for HTML to numpy data
    """
    HTML_WRAPPER = """
<html>
<style>
body {{
    background: #eee;
    color: #0c69c0;
}}
div {{
    background: #50C878;
    padding: 10px;
    border: 2px solid #F4A460;
    border-radius: 5px;
    font-size: 12px;
}}
p {{
    border: 1px solid #00b3f4;
    border-radius: 5px;
    padding: 10px;
}}
a {{
    text-decoration: underline;
    color: #2A52BE;
}}
</style>
{}
</html>
"""

    def __init__(self):
        self.app = QApplication([])
        QWebView.__init__(self)
        self.resize(256, 256)
        self.page().setViewportSize(self.size())

    def render_html(self, html):
        """
        Render HTML to numpy array
        :param html: 
        :return: 
        """
        if html.count('<') != html.count('>'):
            html = ''
        if html.count('<p>') != html.count('</p>'):
            html = ''
        # if html.count('><p'):
        #     html = ''
        # html = '<p>PText</p><a>LinkText</a>'
        self.setHtml(HTMLRenderer.HTML_WRAPPER.format(html))
        frame = self.page().mainFrame()

        # render image
        image = QImage(self.page().viewportSize(), QImage.Format_RGB888)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        image = image.convertToFormat(QImage.Format_RGB888)
        bytes = image.bits().asstring(image.byteCount())

        mode = "RGB"
        pilimg = Image.frombuffer(mode, (image.width(), image.height()), bytes, 'raw', mode, 0, 1)
        # pilimg.show()

        # pilimg.save('test_render2.png')
        return np.array(pilimg), pilimg


class HTMLGame:
    """
    Environment for build HTML and return state for each step
    """
    TEXT_CONTENT_MAP = {
        'button': 'ButtonText',
        'div': 'DivText',
        'p': 'PText',
        'td': 'TableCellText',
        'li': 'ListItemText',
        'a': 'LinkText',
    }

    REWARD = 1.0

    def __init__(self, result_image, renderer):
        self.start_image = result_image
        img = Image.open(self.start_image).convert('L')
        self.result_image = np.array(img) / 255.0
        self.html_covr = HTML2VECConverter()
        self.idx = 0
        self.html_vec = [0, 0, 0, 0, 0, 0]
        self.renderer = renderer

    def reset(self):
        self.__init__(self.start_image, self.renderer)

        html = self.html_covr.convert(self.html_vec, direction=HTML2VECConverter.VEC2HTML_DIRECTION)
        html = self.fill_text_for_html(html)

        # state = np.zeros([100 * 100 * 3, ], dtype=np.float32)
        state = self.renderer.render_html(html) / 255.0
        # state = state.flatten()
        # state = np.concatenate((state, np.array([np.identity(6)[v:v+1] for v in self.html_vec]).flatten()), axis=0)
        # state = np.reshape(state, [1, -1])

        return state, np.array([np.identity(6)[v:v+1] for v in self.html_vec]).flatten()

    @classmethod
    def fill_text_for_html(cls, html):
        for k,v in HTMLGame.TEXT_CONTENT_MAP.items():
            tag = '<{tag}></{tag}>'.format(tag=k)
            tag_text = '<{tag}>{text}</{tag}>'.format(text=v, tag=k)
            html = html.replace(tag, tag_text)
        return html

    def action_sample(self):
        choices = [d for d in HTML2VECConverter.html_int_map.values()]
        choices.pop(0)
        return random.choice(choices)

    def action_samples(self):
        choices = [d for d in HTML2VECConverter.html_int_map.values()]
        choices.pop(0)
        return choices

    def step(self, action=None):
        """
        Render HTML and return state, reward, done for each step
        :param action: 
        :return: 
        """
        # print(self.idx)
        if action is None:
            action = self.action_sample()
        self.html_vec[self.idx] = action
        if self.html_vec[:3] == [2, 1, 3]:
            print('HTML vec: ', self.html_vec)
        html = self.html_covr.convert(self.html_vec, direction=HTML2VECConverter.VEC2HTML_DIRECTION)
        html = self.fill_text_for_html(html)

        state = self.renderer.render_html(html) / 255.0
        dist = distance.braycurtis(self.result_image.flatten(), state.flatten())
        reward = HTMLGame.REWARD if dist < 1e-6 else 0
        if set([2,1,3]) < set(self.html_vec):
            reward = HTMLGame.REWARD/2.0
        if set([4,1,5]) < set(self.html_vec):
            reward = HTMLGame.REWARD/2.0
        # reward = HTMLGame.REWARD if self.html_vec == [2, 1, 3, 4, 1, 5] else 0

        self.idx += 1

        done = False
        if reward == HTMLGame.REWARD:
            done = True
        return state, np.array([np.identity(6)[v:v+1] for v in self.html_vec]).flatten(), reward, done


# s = HTMLRenderer()
# data = s.render('<html><body><p>PText</p></body></html>')
