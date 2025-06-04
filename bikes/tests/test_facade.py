from unittest import TestCase
from unittest.mock import patch, MagicMock
from django.core.exceptions import ValidationError
from bikes.facade import BikeShopFacade


class TestBikeShopFacade(TestCase):
    def test_validate_user_data_valid(self):
        valid_data = {"username": "user", "email": "user@example.com", "password": "secure123"}
        result = BikeShopFacade.validate_user_data(valid_data)
        self.assertTrue(result)

    def test_validate_user_data_missing_fields(self):
        with self.assertRaises(ValidationError):
            BikeShopFacade.validate_user_data({"email": "user@example.com", "password": "123456"})

    def test_validate_user_data_invalid_email(self):
        with self.assertRaises(ValidationError):
            BikeShopFacade.validate_user_data({"username": "user", "email": "invalid@", "password": "123456"})

    def test_validate_user_data_weak_password(self):
        with self.assertRaises(ValidationError):
            BikeShopFacade.validate_user_data({"username": "user", "email": "user@example.com", "password": "123"})

    @patch("bikes.facade.send_mail")
    def test_send_confirmation_email_calls_send_mail(self, mock_send):
        BikeShopFacade.send_confirmation_email("user@example.com")
        mock_send.assert_called_once()

    @patch("bikes.facade.User.objects.create_user")
    @patch("bikes.facade.BikeShopFacade.send_confirmation_email")
    def test_register_user_calls_create_and_sends_email(self, mock_send, mock_create_user):
        mock_create_user.return_value = MagicMock(email="user@example.com")
        user_data = {"username": "user", "email": "user@example.com", "password": "secure123"}
        user = BikeShopFacade.register_user(user_data)
        self.assertEqual(user.email, "user@example.com")
        mock_create_user.assert_called_once()
        mock_send.assert_called_once()

    def test_create_order_regular_bike(self):
        bike = BikeShopFacade.create_order("regular")
        self.assertIn("Regular Frame", bike.parts)

    def test_create_order_electric_bike(self):
        bike = BikeShopFacade.create_order("electric")
        self.assertIn("Electric Frame", bike.parts)
