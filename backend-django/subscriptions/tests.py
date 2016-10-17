from django.test import TestCase, RequestFactory
from django.conf import settings
from django.urls import reverse
# from django.core.management import call_command
from unittest.mock import patch, MagicMock
from .models import Customer
from .views import PaymentView, ProcessPaymentView

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentViewTestCase(TestCase):
    def setUp(self):
        self.request = RequestFactory()
        self.url = reverse('index')

    def test_index(self):
        request = self.request.get(self.url)
        response = PaymentView.as_view()(request)

        self.assertEqual(response.status_code, 200, 'The status code was not 200 :(')

class ProcessPaymentViewTestCase(TestCase):
    fixtures = ['customers.json']

    def setUp(self):
        self.valid_token = stripe.Token.create(
            card={
                'number':'4242424242424242',
                'exp_month':'10',
                'exp_year':'19',
                'cvc':'123'
            },
        )
        self.invalid_token = {
            'id': 'invalid_token'
        }
        self.request = RequestFactory()
        self.url = reverse('payment')

    @patch('subscriptions.models.Customer.objects.create', MagicMock(name='create'))
    def test_success_subscription(self):
        # Create data for request
        data = {
            'stripeToken': self.valid_token.id,
            'email': 'yoelfme@hotmail.com',
            'name': 'Yoel Monzon'
        }

        request = self.request.post(self.url, data)
        response = ProcessPaymentView.as_view()(request)

        # Check the response
        self.assertEqual(response.status_code, 200, 'The status code was not 200 :(')
        self.assertEqual(response.context_data['message'], settings.PAYMENT_MESSAGES['success'], 'The message was not successfully')

        # Check that method create on Customer model was called
        self.assertTrue(Customer.objects.create.called, 'The method create on Customer model was not called')
        self.assertEqual(Customer.objects.create.call_count, 1, 'The method create on Customer model was not called only 1 times')

    @patch('subscriptions.models.Customer.objects.create', MagicMock(name='create'))
    def test_failed_subscription(self):
        data = {
            'stripeToken': self.invalid_token['id'],
            'email': 'yoelfme@hotmail.com',
            'name': 'Yoel Monzon'
        }

        request = self.request.post(self.url, data)
        response = ProcessPaymentView.as_view()(request)

        # Check the response
        self.assertEqual(response.status_code, 200, 'The status code was not 200 :(')
        self.assertEqual(response.context_data['message'], settings.PAYMENT_MESSAGES['failed'], 'The message was not failed')

        # Check that method create on Customer model was not called
        self.assertFalse(Customer.objects.create.called, 'The method create on Customer model was called')
        self.assertEqual(Customer.objects.create.call_count, 0, 'The method create on Customer model was called more than 0 times')

    def test_validation_fields_error(self):
        # Create data to send to request without name field
        data = {
            'stripeToken': self.invalid_token['id'],
            'email': 'yoelfme@hotmail.com'
        }

        request = self.request.post(self.url, data)
        response = ProcessPaymentView.as_view()(request)

        # Check the response
        self.assertEqual(response.status_code, 200, 'The status code was not 200 :(')
        self.assertEqual(response.context_data['message'], settings.PAYMENT_MESSAGES['error_validation'], 'The message was not failed')

    @patch('subscriptions.models.Customer.save', MagicMock(name='save'))
    def test_late_subscribed(self):
        # Create data to send to request
        data = {
            'stripeToken': self.valid_token.id,
            'email': 'yoelfme@gmail.com',
            'name': 'Fransua Estrada'
        }

        request = self.request.post(self.url, data)
        response = ProcessPaymentView.as_view()(request)

        # Check the response
        self.assertEqual(response.status_code, 200, 'The status code was not 200 :(')
        self.assertEqual(response.context_data['message'], settings.PAYMENT_MESSAGES['late_subscribed'], 'The message was not late subscribed')

        # Check that method save on Customer model was called
        self.assertTrue(Customer.save.called, 'The method save on Customer model was not called')
        self.assertEqual(Customer.save.call_count, 1, 'The method save on Customer model was not called only 1 times')

    @patch('subscriptions.models.Customer.save', MagicMock(name='save'))
    def test_already_subscribed(self):
        # Create data to send to request
        data = {
            'stripeToken': self.valid_token.id,
            'email': 'julian@outlook.com',
            'name': 'Julian Hernandez'
        }

        request = self.request.post(self.url, data)
        response = ProcessPaymentView.as_view()(request)

        # Check the response
        self.assertEqual(response.status_code, 200, 'The status code was not 200 :(')
        self.assertEqual(response.context_data['message'], settings.PAYMENT_MESSAGES['already_subscribed'], 'The message was not already subscribed')

        # Check that method save on Customer model was called
        self.assertFalse(Customer.save.called, 'The method save on Customer model was called')
        self.assertEqual(Customer.save.call_count, 0, 'The method save on Customer model was called more than 0 times')
