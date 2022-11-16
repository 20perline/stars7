from fastapi import FastAPI
from stars7.database import Database

app = FastAPI()
database = Database()


@app.get("/home")
def home(total: int = 30):
    data = database.get_draw_data(total)
    data.sort(key=lambda k: k['num'])
    return {'num': data[-1]['num'] + 1, 'total': len(data), 'items': data}


@app.get("/patterns/{num}/{mask}")
def pattern_list(num: int, mask: str):
    patterns = database.get_pattern_list(num, mask)
    total = len(patterns)
    return {'num': num, 'total': total, 'items': patterns}
