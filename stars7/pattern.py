from typing import List
from stars7.round import Round


class Pattern(object):
    def __init__(self, signature: str,
                 predictable: bool, predict_success: bool,
                 round_list: List[Round]) -> None:
        self.signature = signature
        self.predictable = predictable
        self.predict_success = predict_success
        self.round_list = round_list
