from typing import List
from stars7.round import Round
from stars7.rectangle import Rectangle


class Pattern(object):

    def __init__(self, signature: str, strategy: str, predict_success: bool,
                 prediction_num: str, prediction_mask: str, rect: Rectangle,
                 round_list: List[Round], winning_ticket: str = '') -> None:
        self.signature = signature
        self.strategy = strategy
        self.prediction_success = predict_success
        self.prediction_num = prediction_num
        self.prediction_mask = prediction_mask
        self.rect = rect
        self.round_list = round_list
        self.winning_ticket = winning_ticket

    def __str__(self):
        return "Pattern(num=%s[%s], strategy=%s, signature=%s, mask=%s, success=%s)" % (
            self.prediction_num, self.winning_ticket, self.strategy, self.signature,
            self.prediction_mask, self.prediction_success)
