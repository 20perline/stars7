import os

CSV_HEADERS = ['day', 'num', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']
COL_NAMES = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']
KEY_COL_NAMES = ['c1', 'c2', 'c3', 'c4']

ROOT_DIR = os.path.dirname(os.path.realpath(__file__ + '/../'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
DATABASE_PATH = os.path.join(DATA_DIR, 'stars7.db')
BG_PATH = os.path.join(DATA_DIR, 'bg.png')

# image settings
RENDER_ON = True
H_PADDING = 20
V_PADDING = 30
# 边长
CELL_LEN = 50
CELL_HALF_LEN = CELL_LEN / 2

TABLE_ROWS = 25
TABLE_COLS = len(COL_NAMES)
# 预测留白行数 包含在TABLE_ROWS中
PREDICTION_ROWS = 1

LINE_WIDTH = 1
RADIUS = 12
IMG_WIDTH = CELL_LEN * TABLE_COLS + H_PADDING * 2
IMG_HEIGHT = CELL_LEN * TABLE_ROWS + V_PADDING * 2

FIRST_X = H_PADDING + LINE_WIDTH + CELL_HALF_LEN
FIRST_Y = IMG_HEIGHT - V_PADDING - LINE_WIDTH - CELL_HALF_LEN

WATERMARK_X = H_PADDING / 2
WATERMARK_Y = IMG_HEIGHT - V_PADDING / 2

FONT_FILE = os.path.join(os.path.dirname(__file__), 'fonts', 'arial.ttf')
FONT_SIZE = 18
BOLD_FONT_SIZE = 28
