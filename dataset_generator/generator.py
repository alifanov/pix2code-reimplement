import random
import string
import imgkit
import os
from subprocess import call


class Tag:
    CAN_CONTAIN_TEXT_ITEMS = [
        'p',
        'div',
        'td',
        'a',
        'li',
        'button',
    ]
    CONTAINABLE_ITEMS = [
        'p',
        'div',
        # 'tr',
        'table',
        'ul',
        # 'td',
        'a',
    ]
    NON_CONTAINABLE_ITEMS = [
        'button',
        'input',
        'textarea'
    ]
    INPUT_ITEMS = [
        'input',
    ]
    name = ''
    items = []

    def __init__(self, name):
        self.name = name

    def is_containable(self):
        return self.name in self.CONTAINABLE_ITEMS

    def can_contain_text(self):
        return self.name in self.CAN_CONTAIN_TEXT_ITEMS

    def is_input_item(self):
        return self.name in self.INPUT_ITEMS

    def is_can_has_parent(self, parent):
        if parent.name == 'a' and self.name == 'a':
            return False
        if parent.name == 'a' and self.name == 'button':
            return False
        if parent.name == 'a' and self.name == 'textarea':
            return False
        if parent.name == 'a' and self.name == 'input':
            return False
        if parent.name == 'table' and self.name != 'tr':
            return False
        if parent.name == 'tr' and self.name != 'td':
            return False
        if parent.name == 'ul' and self.name != 'li':
            return False
        return True


class DatasetGenerator:
    TEXT_CONTENT_MAP = {
        'button': 'Button',
        'div': 'Lore ipsum Lore ipsum',
        'p': 'PText',
        'td': 'table row',
        'li': 'list items',
        'a': 'This is the link',
    }
    BASE_TEMPLATE = \
"""
<html>
<head>
<style>
body {{
    background: #eee;
    color: #449EF3;
}}
div {{
    background: #50C878;
    padding: 10px;
    margin: 10px;
    border: 2px solid #F4A460;
    border-radius: 5px;
}}
a {{
    text-decoration: underline;
    color: #2A52BE;
}}
</style>
</head>
<body>
{}
</body>
</html>
    """
    ITEM_TEMPLATE = '<{tag}>{items}</{tag}>'
    INPUT_ITEM_TEMPLATE = '<{tag}/>'

    def _clear_empty_tags(self, data):
        for tag in [
            'ul',
            'table',
            'tr',
            'link',
        ]:
            data = data.replace(self.ITEM_TEMPLATE.format(tag=tag, items=''), '')
        return data

    def _render_item(self, item):
        template = self.ITEM_TEMPLATE
        if item.is_input_item():
            template = self.INPUT_ITEM_TEMPLATE

        items = ''

        if item.items:
            items = ''.join([self._render_item(it) for it in item.items])
        elif item.can_contain_text():
            text = self.TEXT_CONTENT_MAP[item.name]
            items = text
        return self._clear_empty_tags(template.format(tag=item.name, items=items))

    def _generate_item(self, depth=3, parent=None):
        if parent == 'table':
            tag_name = 'tr'
        elif parent == 'tr':
            tag_name = 'td'
        else:
            tag_name = random.choice(Tag.CONTAINABLE_ITEMS + Tag.NON_CONTAINABLE_ITEMS)
        item = Tag(name=tag_name)
        if item.is_containable() and depth != 0:
            random_choice = random.randint(0, 15)
            new_items = [self._generate_item(depth=depth - 1, parent=item) for i in range(random_choice)]
            new_items = [n for n in new_items if n.is_can_has_parent(item)]
            item.items = new_items
        return item

    def _get_next_item_name(self):
        files = os.listdir('htmls')
        if not files:
            return 0
        names = [int(f.replace('.html', '')) for f in files]
        return max(names)+1

    def get_next_dataset_item(self):
        next_item_name = self._get_next_item_name()

        new_item = self._generate_item()
        rendered_item = self._render_item(new_item)
        if rendered_item:
            html = self.BASE_TEMPLATE.format(
                rendered_item
            )
            next_html_name = 'htmls/{}.html'.format(next_item_name)
            print(html, file=open(next_html_name, 'w'))

            next_image_name = 'images/{}.jpg'.format(next_item_name)
            call(['phantomjs', 'render_html.js', next_html_name, next_image_name])


if __name__ == "__main__":
    dg = DatasetGenerator()
    dg.get_next_dataset_item()
