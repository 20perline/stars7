from PIL import Image, ImageDraw, ImageFont
from stars7.round import Round
from stars7 import settings
from stars7.utils import random_str
from typing import List
import os


class Render(object):

    def __init__(self, feed) -> None:
        self.feed = feed
        self._draw_background()

    def save(self, round_list: List[Round]):
        # return False
        bg_path = settings.BG_PATH
        if not os.path.exists(bg_path):
            return False
        next_dir = '{}/data/{}'.format(settings.ROOT_DIR, self.feed.next_num)
        if not os.path.exists(next_dir):
            os.mkdir(next_dir)
        filename = '{}/{}.png'.format(next_dir, random_str(5))
        image = Image.open(bg_path)
        draw = ImageDraw.Draw(image)
        radius = settings.RADIUS
        cell_len = settings.CELL_LEN
        for round in round_list:
            for coord in round.coordinates:
                col = settings.COL_NAMES.index(coord.col)
                x = settings.FIRST_X + col * cell_len
                y = settings.FIRST_Y - coord.row * cell_len
                circle_axis = [x-radius, y-radius, x+radius, y+radius]
                draw.ellipse(circle_axis, outline='red', width=1)
        image.save(filename, 'png')

    def _draw_background(self):
        img_width = settings.IMG_WIDTH
        img_height = settings.IMG_HEIGHT
        line_width = settings.LINE_WIDTH
        image = Image.new("RGB", (img_width, img_height), 'white')
        draw = ImageDraw.Draw(image)

        cell_len = settings.CELL_LEN
        black_color = 'black'
        red_color = 'red'
        green_color = 'green'
        # 竖线
        for i in range(settings.TABLE_COLS+1):
            x_axis = settings.H_PADDING + cell_len * i
            start = (x_axis, 0)
            end = (x_axis, img_height)
            if i == 1 or i == 5:
                draw.line([start, end], fill=green_color, width=line_width * 3)
            else:
                draw.line([start, end], fill=black_color, width=line_width)

        first_split_row = self.feed.first_split_row
        # 横线
        for i in range(settings.TABLE_ROWS+1):
            y_axis = img_height - settings.V_PADDING - cell_len * i
            start = (0, y_axis)
            end = (img_width, y_axis)
            first_bold = (first_split_row + 1) % 4
            if i == first_bold or (i - first_bold) % 4 == 0:
                draw.line([start, end], fill=red_color, width=line_width * 3)
            else:
                draw.line([start, end], fill=black_color, width=line_width)

        font = ImageFont.truetype("arial.ttf", settings.FONT_SIZE)
        bold_font = ImageFont.truetype("arial.ttf", settings.BOLD_FONT_SIZE)

        for r in range(settings.TABLE_ROWS):
            for c in range(settings.TABLE_COLS):
                x = settings.FIRST_X + c * cell_len
                y = settings.FIRST_Y - r * cell_len
                val = str(self.feed.get_value_at(r, c))
                if c > 0 and c < 5:
                    draw.text([x, y], text=val, fill=black_color, anchor='mm', font=bold_font)
                else:
                    draw.text([x, y], text=val, fill=black_color, anchor='mm', font=font)

        image.save(settings.BG_PATH, 'png')
