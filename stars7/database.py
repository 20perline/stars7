import json
import sqlite3
import numpy
import pandas as pd
from stars7 import settings
from stars7.pattern import Pattern
from stars7.coordinate import Coordinate
from stars7.round import Round


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, numpy.int64):
            return int(o)
        return o.__dict__


def round_list_to_str(round_list):
    return json.dumps(round_list, cls=MyEncoder).encode('utf8')


def str_to_round_list(json_str):
    round_list = []
    for r in json.loads(json_str):
        coord_list = []
        for coord in r['coordinates']:
            coord_list.append(Coordinate(coord['row'], coord['col']))
        round = Round(r['round_num'], coord_list, r['values'], r['offset'])
        round_list.append(round)
    return round_list


sqlite3.register_adapter(list, round_list_to_str)
# RL = Round List
sqlite3.register_converter('RL', str_to_round_list)


class Database(object):
    _instance = None
    _initiated = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initiated:
            self.conn = sqlite3.connect(settings.DATABASE_PATH,
                                        check_same_thread=False,
                                        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.create_tables()
            self._initiated = True

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self._initiated = False

    def create_tables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS lottery (
            day TEXT,
            num INTEGER,
            c0 INTEGER,
            c1 INTEGER,
            c2 INTEGER,
            c3 INTEGER,
            c4 INTEGER,
            c5 INTEGER,
            c6 INTEGER,
            c7 INTEGER,
            PRIMARY KEY(num)
            )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS pattern (
            signature TEXT,
            prediction_num INTEGER,
            prediction_mask TEXT,
            prediction_success INTEGER,
            strategy TEXT,
            offset INTEGER,
            elements INTEGER,
            winning_ticket TEXT,
            works INTEGER,
            round_list RL,
            PRIMARY KEY(signature, prediction_num)
            )""")

    def get_latest_draw_day(self):
        return self.cursor.execute(
            "select max(day) as day from lottery").fetchone()[0]

    def save_draw_records(self, records):
        self.cursor.executemany(
            "insert or ignore into lottery VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            records)
        self.conn.commit()

    def get_draw_data_frame(self):
        return pd.read_sql_query('select * from lottery order by num desc',
                                 self.conn)

    def get_draw_data(self, total=30):
        return self.cursor.execute(
            'select * from lottery order by num desc').fetchmany(total)

    def save_pattern(self, pattern: Pattern):
        model = {
            'signature': pattern.signature,
            'prediction_num': pattern.prediction_num,
            'prediction_mask': pattern.prediction_mask,
            'prediction_success': pattern.prediction_success,
            'strategy': pattern.strategy,
            'offset': pattern.rect.offset,
            'elements': len(pattern.round_list[0].values),
            'winning_ticket': pattern.winning_ticket,
            'works': len(pattern.round_list) - 1,
            'round_list': pattern.round_list
        }
        self.cursor.execute(
            """insert or ignore into pattern values(:signature, :prediction_num, :prediction_mask, :prediction_success,
                :strategy, :offset, :elements, :winning_ticket, :works, :round_list)
            """, model)
        self.conn.commit()

    def get_pattern_list(self, num, mask):
        return self.cursor.execute(
            "select * from pattern where prediction_num = ? and prediction_mask = ?",
            (num, mask)).fetchall()
