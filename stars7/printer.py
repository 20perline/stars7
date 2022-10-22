from PIL import Image, ImageDraw, ImageFont
from stars7.feed import Feed
from stars7.pattern import Pattern
from stars7 import settings
import os


class Printer(object):

    def __init__(self, feed: Feed) -> None:
        self.feed = feed
        self.font = ImageFont.truetype(settings.FONT_FILE, settings.FONT_SIZE)
        self.bold_font = ImageFont.truetype(settings.FONT_FILE, settings.BOLD_FONT_SIZE)
        self._draw_background()

    def do_print(self, pattern: Pattern):
        if not settings.RENDER_ON:
            return False
        if not pattern.predictable:
            return False
        bg_path = settings.BG_PATH
        if not os.path.exists(bg_path):
            return False
        rounds = len(pattern.round_list)
        next_dir = '{}/data/{}/{}'.format(settings.ROOT_DIR, self.feed.next_num, str(rounds))
        if not os.path.exists(next_dir):
            os.makedirs(next_dir)
        signature = pattern.signature
        filename = '{}/{}.png'.format(next_dir, signature)
        image = Image.open(bg_path)
        draw = ImageDraw.Draw(image)
        prediction_rows = settings.PREDICTION_ROWS
        radius = settings.RADIUS
        cell_len = settings.CELL_LEN
        for round in pattern.round_list:
            values = round.values
            for i, coord in enumerate(round.coordinates):
                col = settings.COL_NAMES.index(coord.col)
                x = settings.FIRST_X + col * cell_len
                y = settings.FIRST_Y - (coord.row + prediction_rows) * cell_len
                circle_axis = [x-radius, y-radius, x+radius, y+radius]
                draw.ellipse(circle_axis, outline='red', width=1)
                if coord.row < 0:
                    draw.text([x, y], str(values[i]), fill='black', anchor='mm', font=self.font)

        draw.text([settings.WATERMARK_X, settings.WATERMARK_Y], signature, fill='red', anchor='mm')
        image.save(filename, 'png')

    def _draw_background(self):
        img_width = settings.IMG_WIDTH
        img_height = settings.IMG_HEIGHT
        line_width = settings.LINE_WIDTH
        prediction_rows = settings.PREDICTION_ROWS
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
            end = (x_axis, img_height - settings.V_PADDING)
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
            first_bold = (first_split_row + prediction_rows + 1) % 4
            if i == first_bold or (i - first_bold) % 4 == 0:
                draw.line([start, end], fill=red_color, width=line_width * 3)
            else:
                draw.line([start, end], fill=black_color, width=line_width)

        for r in range(settings.TABLE_ROWS):
            for c in range(settings.TABLE_COLS):
                x = settings.FIRST_X + c * cell_len
                y = settings.FIRST_Y - r * cell_len
                if r < prediction_rows:
                    val = ''
                else:
                    val = str(self.feed.get_value_at(r - prediction_rows, c))
                if c > 0 and c < 5:
                    draw.text([x, y], text=val, fill=black_color, anchor='mm', font=self.bold_font)
                else:
                    draw.text([x, y], text=val, fill=black_color, anchor='mm', font=self.font)

        image.save(settings.BG_PATH, 'png')
