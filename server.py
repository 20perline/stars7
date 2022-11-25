from fastapi import FastAPI
from stars7.database import Database
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
database = Database()

origins = [
    "http://192.168.0.112:5173",
    "http://localhost:5173",
    "http://175.178.14.16",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
