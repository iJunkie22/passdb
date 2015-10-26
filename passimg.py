import xml.etree.ElementTree as ET
import passdb

__author__ = 'ethan'


def color_from_u(u1):
    assert isinstance(u1, unicode)
    val = ord(u1)
    color_str = '#{:0>3x}'.format(val)
    return color_str


class SVG(object):
    def __init__(self, width=50, height=50):
        self._width = width
        self._height = height
        self._cur_slot = 0
        self.svg_root = ET.Element('svg', {'xmlns': "http://www.w3.org/2000/svg",
                                           'viewBox': "0 0 " + str(width) + " " + str(height),
                                           'width': str(width),
                                           'height': str(height)
                                           }
                                   )

    def update_header(self):
        self.svg_root['viewBox'] = "0 0 " + str(self._width) + " " + str(self._height)
        self.svg_root['width'] = str(self._width)
        self.svg_root['height'] = str(self._height)

    def add_slot(self, fill_hex):
        y_slot, x_slot = divmod(self._cur_slot, self._width)
        new_rect = ET.Element('rect', {'x': str(x_slot),
                                       'y': str(y_slot),
                                       'width': "1",
                                       'height': "1",
                                       'fill': fill_hex}
                              )
        self.svg_root.append(new_rect)
        self._cur_slot += 1

    def next_line_slot(self):
        self._cur_slot += self._width - (self._cur_slot % self._width)


svg1 = SVG()

test_word = passdb.s1a
for l in test_word:
    svg1.add_slot(color_from_u(l))

svg1.next_line_slot()
for l2 in passdb.s2a:
    svg1.add_slot(color_from_u(l2))

print ET.tostring(svg1.svg_root)

