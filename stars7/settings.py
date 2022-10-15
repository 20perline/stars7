import os

CSV_HEADERS = ['day', 'num', 'c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']
COL_NAMES = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7']

ROOT_DIR = os.path.dirname(os.path.realpath(__file__ + '/../'))
DATA_PATH = ROOT_DIR + '/data/dat.csv'
BG_PATH = ROOT_DIR + '/data/bg.png'

# image settings
RENDER_ON = False
H_PADDING = 20
V_PADDING = 20
# 边长
CELL_LEN = 50
CELL_HALF_LEN = CELL_LEN / 2
TABLE_ROWS = 20
TABLE_COLS = len(COL_NAMES)
LINE_WIDTH = 1
RADIUS = 12
IMG_WIDTH = CELL_LEN * TABLE_COLS + H_PADDING * 2
IMG_HEIGHT = CELL_LEN * TABLE_ROWS + V_PADDING * 2

FIRST_X = H_PADDING + LINE_WIDTH + CELL_HALF_LEN
FIRST_Y = IMG_HEIGHT - V_PADDING - LINE_WIDTH - CELL_HALF_LEN

FONT_SIZE = 18
BOLD_FONT_SIZE = 28
