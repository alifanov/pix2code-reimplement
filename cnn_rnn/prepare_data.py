import sys
sys.path.append('..')

import random
import numpy as np
from scipy.misc import toimage
from dataset_generator.html_renderer import HTMLRenderer, HTML2VECConverter, HTMLGame


def generate_dataset():
    renderer = HTMLRenderer()
    converter = HTML2VECConverter()

    for i in range(1000):
        tags = ['<p></p>', '<a></a>', '<div></div>']
        html = '<body>{}{}{}</body>'.format(
            random.choice(tags),
            random.choice(tags),
            random.choice(tags),
        )
        item = converter.convert(html)
        html = HTMLGame.fill_text_for_html(html)
        print(html)
        image_data, image = renderer.render_html(html)
        fname = '-'.join([str(i) for i in item])
        image.save('images/{}.png'.format(fname))
        np.save('images/{}'.format(fname), image_data)

if __name__ == "__main__":
    generate_dataset()