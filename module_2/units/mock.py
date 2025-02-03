import pytest
from unittest.mock import patch


class CreditCard:
    def getCardNumber(self): ...

    def getCardHolder(self): ...

    def getExpiryDate(self): ...

    def getCvv(self): ...

    def charge(amount: float): ...


class PaymentForm:

    def __init__(self, card: CreditCard):
        self.card = card

    def pay(self, amount: float):
        try:
            self.card.charge(amount)
        except Exception as e:
            raise(e)
