import sqlite3
from stars7 import settings
from stars7.pattern import Pattern
import pandas as pd
import numpy
import json


class MyEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, numpy.int64):
            return int(o)
        return o.__dict__


class Database(object):
    _instance = None
    _initiated = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initiated:
            self.conn = sqlite3.connect(settings.DATABASE_PATH)
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
            round_list TEXT,
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
            'round_list': json.dumps(pattern.round_list, cls=MyEncoder),
        }
        self.cursor.execute(
            """insert or ignore into pattern values(:signature, :prediction_num,
                :prediction_mask, :prediction_success,
                :strategy, :offset, :elements, :winning_ticket, :works, :round_list)
            """, model)
        self.conn.commit()
