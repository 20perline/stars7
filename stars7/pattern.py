from typing import List
from stars7.round import Round


class Pattern(object):

    def __init__(self, signature: str, strategy: str,
                 predictable: bool, predict_success: bool,
                 prediction_num: str, prediction_mask: str,
                 round_list: List[Round], winning_ticket: str = '') -> None:
        self.signature = signature
        self.strategy = strategy
        self.predictable = predictable
        self.predict_success = predict_success
        self.prediction_num = prediction_num
        self.prediction_mask = prediction_mask
        self.round_list = round_list
        self.winning_ticket = winning_ticket

    def __str__(self):
        return "Pattern(num=%s[%s], strategy=%s, signature=%s, mask=%s, predictable=%s, predict_success=%s)" % (
            self.prediction_num, self.winning_ticket, self.strategy, self.signature,
            self.prediction_mask, self.predictable, self.predict_success)
