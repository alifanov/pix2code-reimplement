from collections import OrderedDict


class HTML2VECConverter:
    HTML2VEC_DIRECTION = 0
    VEC2HTML_DIRECTION = 1
    html_int_map = {
        # '': 0,
        '>': 1,
        '<p': 2,
        '</p>': 3,
        '<a': 4,
        '</a>': 5,
        '<div': 6,
        '</div>': 7,
        '<body>': 8,
        '</body>': 9,
        # '<input': 10,
        # '</input>': 11,
        # '<button': 12,
        # '</button>': 13,
        # '<textarea': 14,
        # '</textarea>': 15
        # '/>': 4,
        # '': 6,
        # '<table': 9,
        # '</table>': 10,
        # 'class=': 15,
        # '<head': 16,
        # '</head>': 17,
        # '<html': 18,
        # '</html>': 19,
        # '<li': 20,
        # '</li>': 21,
        # '<ul': 22,
        # '</ul>': 23,
        # '<ol': 24,
        # '</ol>': 25,
        # '<tr': 26,
        # '</tr>': 27,
        # '<td': 28,
        # '</td>': 29,
    }


    def __init__(self):
        self.html_int_map = OrderedDict(sorted(self.html_int_map.items(), key=lambda x: x[1]))

    def _clear_data(self, data):
        return data.replace('\n', '')

    def _get_next_item(self, data):
        origin_data = data[::]
        while data:
            for k, v in self.html_int_map.items():
                if data.startswith(k):
                    return k, data[len(k):]
            data = data[1:]
        return None, origin_data

    def split_html(self, data):
        result = []
        html = self._clear_data(data[::])
        while html:
            node, new_html = self._get_next_item(html)
            if node:
                result.append(node)
                html = new_html
        return result

    def convert(self, data, direction=HTML2VEC_DIRECTION):
        result = ''
        if direction == self.HTML2VEC_DIRECTION:
            result = [self.html_int_map[node] for node in self.split_html(data)]
        elif direction == self.VEC2HTML_DIRECTION:
            reversed_map = {v:k for k,v in self.html_int_map.items()}
            result = ''.join([reversed_map[num] for num in data])
        return result
