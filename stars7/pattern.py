from typing import List
from stars7.round import Round


class Pattern(object):
    def __init__(self, index: int, name: str, signature: str,
                 predictable: bool, predict_success: bool,
                 round_list: List[Round]) -> None:
        self.index = index
        self.name = name
        self.signature = signature
        self.predictable = predictable
        self.predict_success = predict_success
        self.round_list = round_list
