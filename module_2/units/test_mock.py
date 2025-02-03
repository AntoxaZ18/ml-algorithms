import pytest
from unittest.mock import patch, MagicMock
from mock import CreditCard, PaymentForm


def test_payment_form_successful_charge():
    """
    Тестирует успешное выполнение charge через PaymentForm.
    """
    # Создаем мок для CreditCard
    mock_card = MagicMock(spec=CreditCard)
    mock_card.charge.return_value = None  # Метод charge ничего не возвращает

    # Создаем экземпляр PaymentForm с моком CreditCard
    payment_form = PaymentForm(card=mock_card)

    payment_form.pay(100.0)  # Пытаемся списать сумму 100.0

    # Проверяем, что метод charge был вызван с правильным аргументом
    mock_card.charge.assert_called_once_with(100.0)


def test_payment_form_exception_handling():
    """
    Тестирует обработку исключения при вызове charge.
    """
    # Создаем мок для CreditCard
    mock_card = MagicMock(spec=CreditCard)
    mock_card.charge.side_effect = ValueError("Charge failed")

    payment_form = PaymentForm(card=mock_card)

    # Проверяем, что исключение передается дальше
    with pytest.raises(ValueError, match="Charge failed"):
        payment_form.pay(100.0)

    # Проверяем, что метод charge был вызван
    mock_card.charge.assert_called_once_with(100.0)
